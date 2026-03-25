---
description: "Odoo data validation - SQL constraints for database-level checks and Python constraints with @api.constrains for complex business rules"
applyTo: "**/models/**/*.py"
---

# Chapter 10: Constraints

## Overview

The previous chapter introduced the ability to add some business logic to our model. We can now link buttons to business code, but how can we prevent users from entering incorrect data? For example, in our real estate module nothing prevents users from setting a negative expected price.

Odoo provides two ways to set up automatically verified invariants: **Python constraints** and **SQL constraints**.

## SQL

Reference: the documentation related to this topic can be found in [Models](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#reference-orm-models) and in the [PostgreSQL's documentation](https://www.postgresql.org/docs/12/ddl-constraints.html).

📝 **Note**: **Goal**: at the end of this section:

Amounts should be (strictly) positive

*Constraints on amounts*

Property types and tags should have a unique name

*Constraints on names*

SQL objects are defined through `Constraint` attributes.

Simple example:

```python
_check_percentage = models.Constraint(
    'CHECK(percentage >= 0 AND percentage <= 100)',
    'The percentage of an analytic distribution should be between 0 and 100.',
)
```

### Exercise: Add SQL Constraints

Add the following constraints to their corresponding models:

- A property expected price must be strictly positive
- A property selling price must be positive
- An offer price must be strictly positive
- A property tag name and property type name must be unique

**Tip**: search for the `unique` keyword in the Odoo codebase for examples of unique names.

Restart the server with the `-u estate` option to see the result. Note that you might have data that prevents a SQL constraint from being set. An error message similar to the following might pop up:

```
ERROR rd-demo odoo.schema: Table 'estate_property_offer': unable to add constraint 'estate_property_offer_check_price' as CHECK(price > 0)
```

For example, if some offers have a price of zero, then the constraint can't be applied. You can delete the problematic data in order to apply the new constraints.

## Python

Reference: the documentation related to this topic can be found in [constrains()](https://www.odoo.com/documentation/19.0/developer/reference/backend/orm.html#odoo.api.constrains).

📝 **Note**: **Goal**: at the end of this section, it will not be possible to accept an offer lower than 90% of the expected price.

*Python constraint*

SQL constraints are an efficient way of ensuring data consistency. However it may be necessary to make more complex checks which require Python code. In this case we need a Python constraint.

A Python constraint is defined as a method decorated with `constrains()` and is invoked on a recordset. The decorator specifies which fields are involved in the constraint. The constraint is automatically evaluated when any of these fields are modified. The method is expected to raise an exception if its invariant is not satisfied:

```python
from odoo.exceptions import ValidationError

...

@api.constrains('date_end')
def _check_date_end(self):
    for record in self:
        if record.date_end < fields.Date.today():
            raise ValidationError("The end date cannot be set in the past")
    # all records passed the test, don't return anything
```

A simple example can be found [here](https://github.com/odoo/odoo/blob/cd9af815ba591935cda367d33a1d090f248dd18d/addons/event/models/event_event.py#L366-L374).

### Exercise: Add Python Constraints

Add a constraint so that the selling price cannot be lower than 90% of the expected price.

**Tip**: the selling price is zero until an offer is validated. You will need to fine tune your check to take this into account.

⚠️ **Warning**: Always use the `float_compare()` and `float_is_zero()` methods from `odoo.tools.float_utils` when working with floats!

Ensure the constraint is triggered every time the selling price or the expected price is changed!

## Performance Considerations

SQL constraints are usually more efficient than Python constraints. When performance matters, always prefer SQL over Python constraints.

Our real estate module is starting to look good. We added some business logic, and now we make sure the data is consistent. However, the user interface is still a bit rough. Let's see how we can improve it in the next chapter.
