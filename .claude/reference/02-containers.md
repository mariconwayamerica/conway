---
description: "Odoo.sh container structure, directory layout, database shell operations, debugging setup, and running Odoo server commands"
applyTo: "**/Dockerfile,**/docker-compose.yml,**/*.sh"
---

# Containers

## Overview

Each build is isolated within its own container (Linux namespaced container).

The base is an Ubuntu system, where all of Odoo's required dependencies, as well as common useful packages, are installed.

If your project requires additional Python dependencies, or more recent releases, you can define a `requirements.txt` file in the root of your branches listing them. The platform will take care to install these dependencies in your containers. The [pip requirements specifiers documentation](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format) can help you write a `requirements.txt` file. To have a concrete example, check out the [requirements.txt file of Odoo](https://github.com/odoo/odoo/blob/master/requirements.txt).

The `requirements.txt` files of submodules are taken into account as well. The platform looks for `requirements.txt` files in each folder containing Odoo modules: Not in the module folder itself, but in their parent folder.

## Directory Structure

As the containers are Ubuntu based, their directory structure follows the linux Filesystem Hierarchy Standard. Ubuntu's filesystem tree overview explains the main directories.

Here are the Odoo.sh pertinent directories:

```
.
├── home
│    └── odoo
│         ├── src
│         │    ├── odoo                Odoo Community source code
│         │    │    └── odoo-bin       Odoo server executable
│         │    ├── enterprise          Odoo Enterprise source code
│         │    ├── themes              Odoo Themes source code
│         │    └── user                Your repository branch source code
│         ├── data
│         │    ├── filestore           database attachments, as well as the files of binary fields
│         │    └── sessions            visitors and users sessions
│         └── logs
│              ├── install.log         Database installation logs
│              ├── odoo.log            Running server logs
│              ├── update.log          Database updates logs
│              └── pip.log             Python packages installation logs
└── usr
     ├── lib
     │    ├── python2.7
     │         └── dist-packages       Python 2.7 standard libraries
     │    ├── python3
     │         └── dist-packages       Python 3 standard libraries
     │    └── python3.5
     │         └── dist-packages       Python 3.5 standard libraries
     ├── local
     │    └── lib
     │         ├── python2.7
     │         │    └── dist-packages  Python 2.7 third-party libraries
     │         └── python3.5
     │              └── dist-packages  Python 3.5 third-party libraries
     └── usr
```

All the Odoo source code is placed under `/home/odoo/src`. The `user` directory contains the source code of your Git repository.

Note that the `enterprise` and `themes` directories are the [Odoo Enterprise](https://github.com/odoo/enterprise) and [Odoo Themes](https://github.com/odoo/design-themes) source code. The latter contains the Website Themes, that is the themes you can choose to style your website made with the Website builder of Odoo.

For instance, if your repository includes a module called `maintenance_extend`, located in the folder `~/user/maintenance`, it can be found in the container filesystem under `/home/odoo/src/user/maintenance/maintenance_extend`.

The `/home/odoo/data` directory contains the module's generated data. Some files in the `filestore` folder can come from modules located in other repositories, such as standard Odoo modules.

The `/home/odoo/logs` folder contains the logs of your server. This allows you to track the behavior of the Odoo process and easily spot errors.

## Database Shell

While accessing a container with the shell, you can access the database using psql.

```bash
$ psql
psql (9.5.2, server 9.5.11)
Type "help" for help.
odoo=>
```

📝 **Note**: Be careful with the `-d` option or the `\c` command. The platforms grants you the right to connect to the database of the build, but you're still able to see other databases available on the PostgreSQL cluster and try connecting to them. However, only the database of your build is accessible; other databases won't work, even if they're listed.

## Running Odoo

### Start the Server

To run Odoo, use:

```bash
$ odoo-bin [options]
```

You can use all the regular Odoo command-line interface (CLI) options. You can see the available options with:

```bash
$ odoo-bin --help
```

Some important options:

```bash
$ odoo-bin -u <module_name>  # Update a specific module
$ odoo-bin -i <module_name>  # Install a specific module
$ odoo-bin -d <database_name>  # Specify database to work with
$ odoo-bin --stop-after-init  # Stop server after modules are loaded
```

### Shell Command

You can also use the Odoo shell to interact with the database programmatically:

```bash
$ odoo-bin shell
```

This gives you an interactive Python shell with access to the Odoo environment. You can use it to query the database, test code, or perform administrative tasks. Example:

```python
>>> env['res.partner'].search([])
>>> partner = env['res.partner'].browse(1)
>>> partner.name
```

## Debugging

### Using a Debugger

You can use pdb, pudb, or ipdb for debugging in Odoo.sh containers.

#### Install debugger (if needed)

```bash
$ pip3 install pudb --user
# or
$ pip3 install ipdb --user
```

#### Adding Breakpoints

Add the following line in your Python code where you want to pause execution:

**Using pdb (built-in):**
```python
import pdb; pdb.set_trace()
```

**Using pudb:**
```python
import pudb; pudb.set_trace()
```

**Using ipdb:**
```python
import ipdb; ipdb.set_trace()
```

When the code reaches this line, execution will pause and you can:
- Inspect variables
- Step through code
- Execute Python commands

### Common Debugger Commands

```
n (next) - Execute current line
s (step) - Step into function
c (continue) - Continue execution
p variable_name - Print variable value
l (list) - Show code around current line
q (quit) - Quit debugger
```

### Logging

You can also use Python's logging module:

```python
import logging
_logger = logging.getLogger(__name__)

_logger.info('Information message')
_logger.warning('Warning message')
_logger.error('Error message')
_logger.debug('Debug message')
```

Logs will appear in `/home/odoo/logs/odoo.log`

## Accessing the Container

You can access a container through the shell. A web shell is available in the container tabs. If you prefer, you can access the container through SSH by using the SSH connection string shown in the container tabs.

Once connected to the container, you have full access to the filesystem and can run commands to:
- Debug issues
- View logs
- Test code
- Run database queries
- Install Python packages for testing

Remember that any changes made directly in the container are temporary and will be lost when the container is rebuilt. Always make permanent changes in your Git repository.
