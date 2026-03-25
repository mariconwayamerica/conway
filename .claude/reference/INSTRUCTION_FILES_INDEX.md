# Odoo.sh Instruction Files Index

This directory contains 32 comprehensive instruction files for Odoo development with GitHub Copilot.

## 📚 File Organization

### Core Module Development (01-16)
- **01** - Your First Module (Module creation, Git workflow, deployment)
- **02** - Containers (Docker structure, psql, debugging)
- **03** - Submodules (Git submodules for external modules)
- **04** - Chapter 1: Architecture Overview (3-tier architecture)
- **05** - Chapter 2: A New Application (Creating from scratch)
- **06** - Chapter 3: Models and Basic Fields (ORM, field types)
- **07** - Chapter 4: Security (Access rights, CSV security)
- **08** - Chapter 5: UI to Play With (Actions, menus, XML)
- **09** - Chapter 6: Basic Views (List, form, search views)
- **10** - Chapter 8: Computed Fields and Onchanges (@api.depends, onchange)
- **11** - Chapter 9: Ready for Some Action (Action buttons, UserError)
- **12** - Chapter 10: Constraints (SQL & Python constraints)
- **13** - Chapter 13: Interact With Other Modules (Link modules, invoices)
- **14** - Chapter 14: QWeb and Kanban Views (Templating engine)
- **15** - Chapter 15: Final Word (Coding standards, runbot)

### Coding Guidelines (16 - Split into 2 parts)
- **16-part1** - Structure (Module organization, file naming, XML format)
- **16-part2** - Conventions (Naming patterns, JS/CSS guidelines)

### Owl Framework & Frontend (17-18, 25-29)
- **17** - Owl Chapter 1: Components (useState, templates, events)
- **18** - Owl Chapter 2: Build Dashboard (Layout, services, useService)
- **25** - Customize Field (Subclass field components, custom widgets)
- **26** - Customize View Type (Extend kanban/list/form views)
- **27** - Create Client Action (Owl components as actions)
- **28** - Standalone Owl Application (Independent Owl apps)
- **29** - Owl on Portal/Website (Frontend integration)

### Advanced Backend (19-24, 30-31)
- **19** - Define Module Data (Master vs demo data, CSV/XML)
- **20** - Safeguard Code with Unit Tests (Test cases, assertions)
- **21** - Write Importable Modules (Proper structuring, __init__)
- **22** - Reuse Code with Mixins (mail.thread, activity.mixin)
- **23** - Build PDF Reports (QWeb reports, paperformat)
- **24** - Write Lean CSS (SCSS best practices, utilities)
- **30** - Multi-company Guidelines (company_id, security isolation)
- **31** - Customized Reports (SQL views, _auto=False, BI)

## 🎯 How to Use

Each file has YAML frontmatter with:
- **description**: What the file teaches
- **applyTo**: Glob patterns for when to apply (e.g., `**/models/**/*.py`)

GitHub Copilot will automatically use these instruction files when working on matching files in your workspace.

## 📊 Stats
- **Total Files**: 32 instruction files
- **Total Size**: ~200KB of Odoo development knowledge
- **Coverage**: Backend Python, Frontend Owl/JS, Views, Reports, Testing, Security

---
Generated: October 9, 2025
