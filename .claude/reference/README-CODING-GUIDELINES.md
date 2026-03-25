# 📘 How Coding Guidelines Work

## 🎯 Three-Tier Instruction System

Your Odoo coding guidelines use a **smart layered approach**:

### 1️⃣ **Always-On Standards** (00-ALWAYS)
```yaml
applyTo: "**/*"  # Applies to EVERY file
```

**What it does:**
- ✅ **Always active** - GitHub Copilot sees this in EVERY file you edit
- 📋 **Concise** (4.5KB) - Quick reference, essential rules only
- 🎯 **Core principles** - Naming, patterns, critical do's/don'ts

**Think of it as:** Your coding "conscience" - always reminding you of best practices.

---

### 2️⃣ **Detailed Structure Guidelines** (16-part1)
```yaml
applyTo: "**/__manifest__.py, **/models/**/*.py, **/views/**/*.xml, ..."
```

**What it does:**
- 🎓 **Context-aware** - Only applies when editing relevant files
- 📚 **Comprehensive** (27KB) - Deep-dive into module structure
- 📁 **Topics**: File organization, directory structure, XML formatting, manifest configuration

**Think of it as:** Your "reference manual" - appears when you need detailed guidance.

---

### 3️⃣ **Detailed Convention Guidelines** (16-part2)
```yaml
applyTo: "**/models/**/*.py, **/static/**/*.js, **/static/**/*.css, ..."
```

**What it does:**
- 🎓 **Context-aware** - Only applies when editing Python/JS/CSS
- 📚 **Comprehensive** (12KB) - Deep-dive into conventions
- 🏷️ **Topics**: Naming patterns, method conventions, JS/CSS best practices

**Think of it as:** Your "style guide" - appears when writing code.

---

## 💡 Why This Works

### **Memory Efficiency:**
- Copilot doesn't load ALL 39KB of guidelines for every file
- Instead: 4.5KB always + relevant context (27KB or 12KB) when needed

### **No "Forgetting":**
The `00-ALWAYS` file ensures Copilot **never forgets** core standards because:
- It matches **every file** (`applyTo: "**/*"`)
- It's loaded for **every single request**
- It's concise enough to always fit in context

### **Best of Both Worlds:**
- ✅ Quick essential reminders (always)
- ✅ Deep detailed guidance (when relevant)
- ✅ No context overload

---

## 🧪 How to Test

1. **Edit a Python model file** (`models/sale_order.py`):
   - Copilot sees: 00-ALWAYS + 16-part1 + 16-part2 (~44KB total)

2. **Edit an XML view** (`views/sale_order_views.xml`):
   - Copilot sees: 00-ALWAYS + 16-part1 (~32KB total)

3. **Edit a JavaScript file** (`static/src/components/dashboard.js`):
   - Copilot sees: 00-ALWAYS + 16-part2 (~17KB total)

4. **Edit ANY file** (even `README.md`):
   - Copilot sees: 00-ALWAYS (~4.5KB)

---

## ✅ Conclusion

**You don't need to remind Copilot every 5 requests!**

The `applyTo: "**/*"` pattern ensures the core standards are **ALWAYS** in context. It's like having a persistent checklist that never goes away.

Think of it like:
- 🧠 **00-ALWAYS** = Your brain's "working memory" (always there)
- 📚 **16-part1/2** = Your brain's "long-term memory" (accessed when needed)

---

**Pro Tip**: If you find Copilot still missing something, add it to the `00-ALWAYS` file - it's guaranteed to be seen!
