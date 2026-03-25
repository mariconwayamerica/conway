---
description: "Odoo coding guidelines Part 2 - naming conventions, symbols, method patterns, JavaScript guidelines, CSS/SCSS best practices"
applyTo: "**/models/**/*.py,**/static/**/*.js,**/static/**/*.css,**/static/**/*.scss"
---

Symbols and Conventions
Model name (using the dot notation, prefix by the module name) :
When defining an Odoo Model : use singular form of the name (res.partner and sale.order instead of res.partnerS and saleS.orderS)

When defining an Odoo Transient (wizard) : use <related_base_model>.<action> where related_base_model is the base model (defined in models/) related to the transient, and action is the short name of what the transient do. Avoid the wizard word. For instance : account.invoice.make, project.task.delegate.batch, …

When defining report model (SQL views e.i.) : use <related_base_model>.report.<action>, based on the Transient convention.

Odoo Python Class : use Pascal case (Object-oriented style).

class AccountInvoice(models.Model):
    ...
Variable name :
use Pascal case for model variable

use underscore lowercase notation for common variable.

suffix your variable name with _id or _ids if it contains a record id or list of id. Don’t use partner_id to contain a record of res.partner

Partner = self.env['res.partner']
partners = Partner.browse(ids)
partner_id = partners[0].id
One2Many and Many2Many fields should always have _ids as suffix (example: sale_order_line_ids)

Many2One fields should have _id as suffix (example : partner_id, user_id, …)

Method conventions
Compute Field : the compute method pattern is _compute_<field_name>

Search method : the search method pattern is _search_<field_name>

Default method : the default method pattern is _default_<field_name>

Selection method: the selection method pattern is _selection_<field_name>

Onchange method : the onchange method pattern is _onchange_<field_name>

Constraint method : the constraint method pattern is _check_<constraint_name>

Action method : an object action method is prefix with action_. Since it uses only one record, add self.ensure_one() at the beginning of the method.

In a Model attribute order should be
Private attributes (_name, _description, _inherit, …)

Default method and default_get

Field declarations

SQL constraints and indexes

Compute, inverse and search methods in the same order as field declaration

Selection method (methods used to return computed values for selection fields)

Constrains methods (@api.constrains) and onchange methods (@api.onchange)

CRUD methods (ORM overrides)

Action methods

And finally, other business methods.

class Event(models.Model):
    # Private attributes
    _name = 'event.event'
    _description = 'Event'

    # Default methods
    def _default_name(self):
        ...

    # Fields declaration
    name = fields.Char(string='Name', default=_default_name)
    seats_reserved = fields.Integer(string='Reserved Seats', store=True
        readonly=True, compute='_compute_seats')
    seats_available = fields.Integer(string='Available Seats', store=True
        readonly=True, compute='_compute_seats')
    price = fields.Integer(string='Price')
    event_type = fields.Selection(string="Type", selection='_selection_type')

    # compute and search fields, in the same order of fields declaration
    @api.depends('seats_max', 'registration_ids.state', 'registration_ids.nb_register')
    def _compute_seats(self):
        ...

    @api.model
    def _selection_type(self):
        return []

    # Constraints and onchanges
    @api.constrains('seats_max', 'seats_available')
    def _check_seats_limit(self):
        ...

    @api.onchange('date_begin')
    def _onchange_date_begin(self):
        ...

    # CRUD methods (and name_search, _search, ...) overrides
    @api.model
    def create(self, vals_list):
        ...

    # Action methods
    def action_validate(self):
        self.ensure_one()
        ...

    # Business methods
    def mail_user_confirm(self):
        ...
Javascript
Static files organization
Odoo addons have some conventions on how to structure various files. We explain here in more details how web assets are supposed to be organized.

The first thing to know is that the Odoo server will serve (statically) all files located in a static/ folder, but prefixed with the addon name. So, for example, if a file is located in addons/web/static/src/js/some_file.js, then it will be statically available at the url your-odoo-server.com/web/static/src/js/some_file.js

The convention is to organize the code according to the following structure:

static: all static files in general

static/lib: this is the place where js libs should be located, in a sub folder. So, for example, all files from the jquery library are in addons/web/static/lib/jquery

static/src: the generic static source code folder

static/src/css: all css files

static/fonts

static/img

static/src/js

static/src/js/tours: end user tour files (tutorials, not tests)

static/src/scss: scss files

static/src/xml: all qweb templates that will be rendered in JS

static/tests: this is where we put all test related files.

static/tests/tours: this is where we put all tour test files (not tutorials).

Javascript coding guidelines
use strict; is recommended for all javascript files

Use a linter (jshint, …)

Never add minified Javascript Libraries

Use Pascal case for class declaration

More precise JS guidelines are detailed in the github wiki. You may also have a look at existing API in Javascript by looking Javascript References.

CSS and SCSS
Syntax and Formatting
SCSS
CSS
.o_foo, .o_foo_bar, .o_baz {
   height: $o-statusbar-height;

   .o_qux {
      height: $o-statusbar-height * 0.5;
   }
}

.o_corge {
   background: $o-list-footer-bg-color;
}
four (4) space indents, no tabs;

columns of max. 80 characters wide;

opening brace ({): empty space after the last selector;

closing brace (}): on its own new line;

one line for each declaration;

meaningful use of whitespace.

Suggested Stylelint settings
Properties order
Order properties from the “outside” in, starting from position and ending with decorative rules (font, filter, etc.).

Scoped SCSS variables and CSS variables must be placed at the very top, followed by an empty line separating them from other declarations.

.o_element {
   $-inner-gap: $border-width + $legend-margin-bottom;

   --element-margin: 1rem;
   --element-size: 3rem;

   @include o-position-absolute(1rem);
   display: block;
   margin: var(--element-margin);
   width: calc(var(--element-size) + #{$-inner-gap});
   border: 0;
   padding: 1rem;
   background: blue;
   font-size: 1rem;
   filter: blur(2px);
}
Naming Conventions
Naming conventions in CSS are incredibly useful in making your code more strict, transparent and informative.

Avoid id selectors, and prefix your classes with o_<module_name>, where <module_name> is the technical name of the module (sale, im_chat, …) or the main route reserved by the module (for website modules mainly, i.e. : o_forum for the website_forum module).
The only exception for this rule is the webclient: it simply uses the o_ prefix.
Avoid creating hyper-specific classes and variable names. When naming nested elements, opt for the “Grandchild” approach.

 Example

Don’t

<div class=“o_element_wrapper”>
   <div class=“o_element_wrapper_entries”>
      <span class=“o_element_wrapper_entries_entry”>
         <a class=“o_element_wrapper_entries_entry_link”>Entry</a>
      </span>
   </div>
</div>
Do

<div class=“o_element_wrapper”>
   <div class=“o_element_entries”>
      <span class=“o_element_entry”>
         <a class=“o_element_link”>Entry</a>
      </span>
   </div>
</div>
Besides being more compact, this approach eases maintenance because it limits the need of renaming when changes occur at the DOM.

SCSS Variables
Our standard convention is $o-[root]-[element]-[property]-[modifier], with:

$o-
The prefix.

[root]
Either the component or the module name (components take priority).

[element]
An optional identifier for inner elements.

[property]
The property/behavior defined by the variable.

[modifier]
An optional modifier.

 Example

$o-block-color: value;
$o-block-title-color: value;
$o-block-title-color-hover: value;
SCSS Variables (scoped)
These variables are declared within blocks and are not accessible from the outside. Our standard convention is $-[variable name].

 Example

.o_element {
   $-inner-gap: compute-something;

   margin-right: $-inner-gap;

   .o_element_child {
      margin-right: $-inner-gap * 0.5;
   }
}
 See also

Variables scope on the SASS Documentation

SCSS Mixins and Functions
Our standard convention is o-[name]. Use descriptive names. When naming functions, use verbs in the imperative form (e.g.: get, make, apply…).

Name optional arguments in the scoped variables form, so $-[argument].

 Example

@mixin o-avatar($-size: 1.5em, $-radius: 100%) {
   width: $-size;
   height: $-size;
   border-radius: $-radius;
}

@function o-invert-color($-color, $-amount: 100%) {
   $-inverse: change-color($-color, $-hue: hue($-color) + 180);

   @return mix($-inverse, $-color, $-amount);
}
 See also

Mixins on the SASS Documentation

Functions on the SASS Documentation

CSS Variables
In Odoo, the use of CSS variables is strictly DOM-related. Use them to contextually adapt the design and layout.

Our standard convention is BEM, so --[root]__[element]-[property]--[modifier], with:

[root]
Either the component or the module name (components take priority).

[element]
An optional identifier for inner elements.

[property]
The property/behavior defined by the variable.

[modifier]
An optional modifier.

 Example

.o_kanban_record {
   --KanbanRecord-width: value;
   --KanbanRecord__picture-border: value;
   --KanbanRecord__picture-border--active: value;
}

// Adapt the component when rendered in another context.
.o_form_view {
   --KanbanRecord-width: another-value;
   --KanbanRecord__picture-border: another-value;
   --KanbanRecord__picture-border--active: another-value;
}
Use of CSS Variables
In Odoo, the use of CSS variables is strictly DOM-related, meaning that are used to contextually adapt the design and layout rather than to manage the global design-system. These are typically used when a component’s properties can vary in specific contexts or in other circumstances.

We define these properties inside the component’s main block, providing default fallbacks.

 Example

my_component.scss
.o_MyComponent {
   color: var(--MyComponent-color, #313131);
}
my_dashboard.scss
.o_MyDashboard {
   // Adapt the component in this context only
   --MyComponent-color: #017e84;
}
 See also

CSS variables on MDN web docs

CSS and SCSS Variables
Despite being apparently similar, CSS and SCSS variables behave very differently. The main difference is that, while SCSS variables are imperative and compiled away, CSS variables are declarative and included in the final output.

 See also

CSS/SCSS variables difference on the SASS Documentation

In Odoo, we take the best of both worlds: using the SCSS variables to define the design-system while opting for the CSS ones when it comes to contextual adaptations.

The implementation of the previous example should be improved by adding SCSS variables in order to gain control at the top-level and ensure consistency with other components.

 Example

secondary_variables.scss
$o-component-color: $o-main-text-color;
$o-dashboard-color: $o-info;
// [...]
component.scss
.o_component {
   color: var(--MyComponent-color, #{$o-component-color});
}
dashboard.scss
.o_dashboard {
   --MyComponent-color: #{$o-dashboard-color};
}
The :root pseudo-class
Defining CSS variables on the :root pseudo-class is a technique we normally don’t use in Odoo’s UI. The practice is commonly used to access and modify CSS variables globally. We perform this using SCSS instead.

Exceptions to this rule should be fairly apparent, such as templates shared across bundles that require a certain level of contextual awareness in order to be rendered properly.