---
description: "Final Odoo development guidelines - code refactoring, coding standards, and testing with runbot"
applyTo: "**/*.py,**/*.xml,**/*.js,**/*.css,**/*.scss"
---

# Chapter 15: The Final Word

## Coding guidelines

We will start refactoring the code to match to the Odoo coding guidelines. The guidelines aim to improve the quality of the Odoo Apps code.

Reference: you will find the Odoo coding guidelines in [Coding guidelines](https://www.odoo.com/documentation/19.0/contributing/development/coding_guidelines.html).

### Exercise: Polish your code

Refactor your code to respect the coding guidelines. Don't forget to run your linter and respect the module structure, the variable names, the method name convention, the model attribute order and the xml ids.

## Test on the runbot

Odoo has its own CI server named runbot. All commits, branches and PR will be tested to avoid regressions or breaking of the stable versions. All the runs that pass the tests are deployed on their own server with demo data.

### Exercise: Play with the runbot

Feel free to go to the [runbot website](https://runbot.odoo.com/) and open the last stable version of Odoo to check out all the available applications and functionalities.
