import base64
import hashlib
import hmac
import logging
import time
import urllib.parse
import uuid

import requests

from odoo import models

_logger = logging.getLogger(__name__)


class NetsuiteConnector(models.AbstractModel):
    _name = 'netsuite.connector'
    _description = 'NetSuite REST API Connector (TBA OAuth 1.0a)'

    # ------------------------------------------------------------------
    # Config helpers
    # ------------------------------------------------------------------

    def _ns_param(self, key):
        return self.env['ir.config_parameter'].sudo().get_param(key)

    def _ns_base_url(self):
        account_id = self._ns_param('netsuite.account_id') or ''
        # NetSuite requires dashes in the subdomain, not underscores
        url_account = account_id.lower().replace('_', '-')
        return f'https://{url_account}.suitetalk.api.netsuite.com/services/rest'

    # ------------------------------------------------------------------
    # OAuth 1.0a / TBA signing
    # ------------------------------------------------------------------

    def _ns_auth_header(self, method, url):
        account_id   = self._ns_param('netsuite.account_id')      or ''
        consumer_key = self._ns_param('netsuite.consumer_key')     or ''
        cons_secret  = self._ns_param('netsuite.consumer_secret')  or ''
        token_id     = self._ns_param('netsuite.token_id')         or ''
        token_secret = self._ns_param('netsuite.token_secret')     or ''

        timestamp = str(int(time.time()))
        nonce     = uuid.uuid4().hex

        oauth_params = {
            'oauth_consumer_key':     consumer_key,
            'oauth_nonce':            nonce,
            'oauth_signature_method': 'HMAC-SHA256',
            'oauth_timestamp':        timestamp,
            'oauth_token':            token_id,
            'oauth_version':          '1.0',
        }

        # Percent-encode and sort params for base string
        encoded_params = '&'.join(
            f'{urllib.parse.quote(k, safe="")}={urllib.parse.quote(v, safe="")}'
            for k, v in sorted(oauth_params.items())
        )
        base_string = '&'.join([
            method.upper(),
            urllib.parse.quote(url, safe=''),
            urllib.parse.quote(encoded_params, safe=''),
        ])

        signing_key = (
            urllib.parse.quote(cons_secret, safe='')
            + '&'
            + urllib.parse.quote(token_secret, safe='')
        )
        raw_sig = hmac.new(
            signing_key.encode('ascii'),
            base_string.encode('ascii'),
            hashlib.sha256,
        ).digest()
        signature = base64.b64encode(raw_sig).decode()

        oauth_params['oauth_signature'] = signature
        # realm must be the account ID in upper-case with underscores
        realm = account_id.upper().replace('-', '_')

        header_parts = [f'realm="{realm}"'] + [
            f'{k}="{urllib.parse.quote(v, safe="")}"'
            for k, v in sorted(oauth_params.items())
        ]
        return 'OAuth ' + ', '.join(header_parts)

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    def netsuite_find_po_id(self, doc_number):
        """Return the NetSuite internal ID of a Purchase Order by its document number (tranId).

        Returns the string ID, or None if not found.
        """
        base_url = self._ns_base_url()
        url = f'{base_url}/query/v1/suiteql'

        # Escape single quotes to prevent SuiteQL injection
        safe_doc = doc_number.replace("'", "''")
        payload = {
            'q': (
                "SELECT id FROM transaction "
                f"WHERE type = 'PurchOrd' AND tranId = '{safe_doc}'"
            )
        }

        headers = {
            'Authorization': self._ns_auth_header('POST', url),
            'Content-Type':  'application/json',
            'Prefer':        'transient',
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        items = resp.json().get('items', [])
        if not items:
            _logger.warning(
                'NetSuite: no PO found with document number %r', doc_number
            )
            return None

        return str(items[0]['id'])

    def netsuite_transform_po_to_bill(self, po_internal_id, memo=None):
        """Transform a NetSuite Purchase Order into a Vendor Bill.

        Returns the new Vendor Bill's internal ID string.
        """
        base_url = self._ns_base_url()
        url = (
            f'{base_url}/record/v1/purchaseOrder'
            f'/{po_internal_id}/!transform/vendorBill'
        )

        headers = {
            'Authorization': self._ns_auth_header('POST', url),
            'Content-Type':  'application/json',
        }

        body = {'memo': memo} if memo else {}
        resp = requests.post(url, json=body, headers=headers, timeout=30)
        resp.raise_for_status()

        # NetSuite returns the new record URL in the Location header
        location = resp.headers.get('Location', '')
        bill_id  = location.rstrip('/').split('/')[-1] if location else 'unknown'

        _logger.info(
            'NetSuite: PO %s transformed to Vendor Bill %s', po_internal_id, bill_id
        )
        return bill_id

    def netsuite_find_so_from_po(self, po_internal_id):
        """Return the NetSuite internal ID of the Sales Order that created this PO.

        GETs the purchaseOrder record and reads the createdFrom link from the
        response body.  Returns the string ID, or None if not found.
        """
        base_url = self._ns_base_url()
        url = f'{base_url}/record/v1/purchaseOrder/{po_internal_id}'

        headers = {
            'Authorization': self._ns_auth_header('GET', url),
            'Content-Type':  'application/json',
        }

        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()

        body = resp.json()
        _logger.debug('NetSuite PO %s record: %s', po_internal_id, body)

        created_from = body.get('createdFrom') or {}
        so_id = created_from.get('id') if isinstance(created_from, dict) else created_from
        if not so_id:
            _logger.warning('NetSuite: PO %s has no createdFrom Sales Order', po_internal_id)
            return None

        return str(so_id)

    def netsuite_create_item_fulfillment(self, so_internal_id):
        """Create an Item Fulfillment from a NetSuite Sales Order (dropship).

        Returns the new Item Fulfillment's internal ID string.
        """
        base_url = self._ns_base_url()
        url = (
            f'{base_url}/record/v1/salesOrder'
            f'/{so_internal_id}/!transform/itemFulfillment'
        )

        headers = {
            'Authorization': self._ns_auth_header('POST', url),
            'Content-Type':  'application/json',
        }

        resp = requests.post(url, json={}, headers=headers, timeout=30)
        if not resp.ok:
            _logger.error('NetSuite Item Fulfillment error %s: %s', resp.status_code, resp.text)
        resp.raise_for_status()

        location = resp.headers.get('Location', '')
        fulfillment_id = location.rstrip('/').split('/')[-1] if location else 'unknown'

        _logger.info(
            'NetSuite: SO %s transformed to Item Fulfillment %s', so_internal_id, fulfillment_id
        )
        return fulfillment_id
