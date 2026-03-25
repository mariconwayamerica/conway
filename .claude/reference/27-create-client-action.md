---
description: "Creating Odoo client actions - Owl components as actions, action registry, custom interfaces, URL routing"
applyTo: "**/static/src/**/*.js,**/static/src/**/*.xml,**/__manifest__.py"
---

Create a client action
A client action triggers an action that is entirely implemented in the client side. One of the benefits of using a client action is the ability to create highly customized interfaces with ease. A client action is typically defined by an OWL component; we can also use the web framework and use services, core components, hooks,…

Create the client action, don’t forget to make it accessible.

<record model="ir.actions.client" id="my_client_action">
    <field name="name">My Client Action</field>
    <field name="tag">my_module.MyClientAction</field>
</record>
Create a component that represents the client action.

my_client_action.js
import { registry } from "@web/core/registry";

import { Component } from  "@odoo/owl";

class MyClientAction extends Component {
    static template = "my_module.clientaction";
}

// remember the tag name we put in the first step
registry.category("actions").add("my_module.MyClientAction", MyClientAction);
my_client_action.xml
<?xml version="1.0" encoding="UTF-8" ?>
<templates xml:space="preserve">
    <t t-name="awesome_tshirt.clientaction">
        Hello world
    </t>
</templates>