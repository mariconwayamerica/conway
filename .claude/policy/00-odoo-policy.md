# Odoo Development Policy (Concise)

Purpose: High-signal, enforceable rules to guide coding in this repo. Cursor should prefer these over longer references.

## Project Structure
- Use one addon per business concern. Keep modules small and cohesive.
- Mandatory files: `__manifest__.py`, `__init__.py`, and appropriately structured `models/`, `views/`, `security/`, `data/`.
- Name addons with clear, lowercase, underscore-separated identifiers.

## Models & Fields
- Prefer explicit types and `required=True` where applicable.
- Use `compute` with `store=True` only when needed for search/performance. Include accurate `depends`.
- Use `onchange` for UI-only reactivity; never rely on it for invariants.
- Default values via `default=` or `@api.model_create_multi` in `create`.
- Relations: set `ondelete` explicitly. Avoid cascades unless correct by design.

## Business Logic
- Keep invariants in model methods, not wizards or controllers.
- Override `create`/`write` sparingly; always call `super()` and maintain constraints.
- Use domain filters and computed helpers over raw SQL where possible.

## Constraints & Validation
- Prefer Python constraints with `@api.constrains` for business logic.
- Use SQL constraints for uniqueness and database-level guarantees.
- Always provide clear error messages with `_()` for i18n.

## Security
- Enforce least privilege. Define `ir.model.access.csv` and record rules per model.
- No business logic in `sudo()` context unless strictly necessary; document rationale.
- Never expose internal fields via `read_group`/`search_read` without review.

## Views & UI
- Keep XML views minimal. Use `xpath` for targeted overrides; avoid duplication.
- Use `list` views (tag: `<list>`); do not use legacy `<tree>`.
- Separate form/list/search views. Use `groups` attributes for role-based visibility.
- QWeb: don't execute complex logic in templates; compute in Python.

## Odoo v19 View Requirements (Critical)
**Search Views:**
- Never use `filter_domain` attribute on `<field>` elements (removed in v19).
- Never use `string` attribute on `<search>` root or `<group>` elements.
- Never use `expand` attribute on `<group>` elements.
- Computed fields used in filter domains MUST have `store=True` to be searchable.
- Use bare `<separator/>` between filter groups; no attributes needed.

**Kanban Views:**
- Use `t-name="card"` for kanban templates (not `t-name="kanban-box"`).
- Always include required fields in the kanban field list before templates.

**List Views:**
- Always use `<list>` tag, never `<tree>` (deprecated).
- In actions, use `view_mode="list,form"` not `view_mode="tree,form"`.

**Settings Extensions:**
- Avoid extending `res.config.settings` views via xpath in v19 (structure changed).
- Prefer standalone menu items or dedicated configuration wizards.

## Reuse & Conventions
- Prefer mixins/utilities for shared behaviors. Avoid copy-paste across addons.
- Follow naming conventions: methods `action_*` for buttons; `name_get`, `name_search` for identity.
- Keep modules importable and side-effect free at import time.

## Testing
- Add unit tests for business invariants and critical flows.
- Seed test data via `data/` or factories; tests must be idempotent.
- Avoid sleeps and external side effects; mock integrations.

## OWL/Frontend (if applicable)
- Components are small and pure; state lives high, props flow down.
- Template logic is simple; heavy lifting in JS/TS.
- Use services for cross-cutting concerns; avoid global mutable state.

## Performance
- Batch operations (`write`, `create`) and use `@api.model_create_multi`.
- Use `search_read`, `read_group` judiciously with indexed fields.
- Add indexes for frequently filtered fields; avoid N+1 queries.

## Documentation
- Include a short README per addon: purpose, key models, important flows.
- Document non-obvious decisions and security implications inline.

