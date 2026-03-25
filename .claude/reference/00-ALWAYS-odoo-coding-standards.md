---
description: "ALWAYS APPLY: Core Odoo coding standards and best practices that should be followed in all Odoo development work"
applyTo: "**/*"
---

# Odoo Coding Standards - Always Apply

⚠️ **These standards apply to ALL Odoo development across the entire codebase.**

## 🎯 Universal Rules

### Python Code Standards

**Naming Conventions:**
- Models: Use singular form with dot notation (e.g., `res.partner`, `sale.order`)
- Variables: Use `underscore_lowercase` notation
- Classes: Use `PascalCase` (e.g., `AccountInvoice`)
- Methods: Use `underscore_lowercase` (e.g., `_compute_total`)
- Private methods: Prefix with underscore `_` (e.g., `_check_values`)
- Public methods: No underscore, callable from UI (e.g., `action_confirm`)

**Field Naming:**
- Many2one fields: suffix with `_id` (e.g., `partner_id`, `user_id`)
- One2many/Many2many: suffix with `_ids` (e.g., `line_ids`, `tag_ids`)
- Boolean fields: prefix with `is_` or `has_` when appropriate

**Method Patterns:**
- Compute: `_compute_<field_name>`
- Inverse: `_inverse_<field_name>`
- Search: `_search_<field_name>`
- Onchange: `_onchange_<field_name>`
- Constraint: `_check_<constraint_name>`
- Default: `_default_<field_name>`
- Action: `action_<action_name>` (and use `self.ensure_one()`)

**Model Attribute Order:**
1. Private attributes (`_name`, `_description`, `_inherit`, `_order`)
2. Default methods (`_default_*`)
3. Field declarations
4. Compute/inverse/search methods
5. Constrains and onchange methods
6. CRUD methods (create, write, unlink overrides)
7. Action methods
8. Other business methods

### XML Standards

**Formatting:**
- Place `id` before `model` in `<record>` tags
- For fields: `name` first, then value, then other attributes
- Group records by model type
- Use meaningful external IDs: `<module>_<model>_<description>`

**Naming Convention for XML IDs:**
- Views: `view_<model>_<view_type>` (e.g., `view_partner_form`)
- Actions: `action_<model>_<description>` (e.g., `action_partner_open`)
- Menu: `menu_<model>_<description>`
- Groups: `group_<description>`

### Security & Best Practices

**Always:**
- ✅ Add access rights (`ir.model.access.csv`) for every model
- ✅ Use `self.ensure_one()` in methods that work on single records
- ✅ Loop over `self` assuming multiple records: `for record in self:`
- ✅ Return something from public methods (at minimum `return True`)
- ✅ Use `@api.depends()` for computed fields
- ✅ Use `@api.constrains()` for validation
- ✅ Propagate context properly with `with_context()`

**Never:**
- ❌ Call `cr.commit()` or `cr.rollback()` (framework handles transactions)
- ❌ Use mutable default arguments (use `None` and set in method)
- ❌ Hardcode business logic without making it extendable
- ❌ Catch bare `Exception` (be specific about error types)
- ❌ Use `partner_id` variable to store a record (use `partner` instead)

### File Organization

**Required Structure:**
```
module_name/
├── __init__.py
├── __manifest__.py
├── models/          # Python model files
├── views/           # XML view files
├── security/        # Access rights & rules
├── data/            # Master data
├── demo/            # Demo data
├── static/src/      # JS, CSS, images
├── controllers/     # HTTP controllers
├── wizard/          # Transient models
└── report/          # Reports & SQL views
```

**File Naming:**
- Models: `<model_name>.py` (e.g., `sale_order.py`)
- Views: `<model_name>_views.xml`
- Security: `ir.model.access.csv`, `<model>_security.xml`
- Data: `<model_name>_data.xml`

## 🚨 Critical Reminders

1. **Test your code**: Always consider edge cases
2. **Performance**: Avoid N+1 queries, use `read()` or `mapped()` efficiently
3. **Translations**: Use `_("string")` for user-facing text
4. **Multi-company**: Consider `company_id` and `allowed_company_ids`
5. **Extendability**: Write small, focused methods that can be overridden

## 📖 Quick Reference

**Common Decorators:**
- `@api.model` - Class method, no recordset context
- `@api.depends('field1', 'field2')` - Computed field dependencies
- `@api.constrains('field1', 'field2')` - Validation constraints
- `@api.onchange('field')` - UI-only field changes

**Common Exceptions:**
- `UserError` - User-facing error message
- `ValidationError` - Validation failed (constraints)
- `AccessError` - Access rights violation

---

💡 **Remember**: These standards ensure code quality, maintainability, and consistency across the entire Odoo ecosystem.
