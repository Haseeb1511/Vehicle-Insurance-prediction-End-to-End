# Vehicle-Insurance-prediction-End-to-End
## 📌 Note: Using `-e .` in `requirements.txt`

✅ **What does `-e .` mean?**  
It means: *“Install this local project in editable mode.”*

When you use `-e .`:
- `pip` expects to find **either**:
  - A valid `setup.py` file **or**
  - A valid `pyproject.toml` file with a `[build-system]` section

---

✅ **Why is this needed?**  
An editable install tells `pip`:
> “Install the local source code as a Python package, so that edits to your code are immediately reflected in your environment.”

To do this, `pip` needs to know:
- 📦 What’s your package name?  
- 📂 Where is the source code?  
- 🗂️ Which files should be included?

This info comes from `setup.py` or `pyproject.toml`.

---

❌ **If your project is NOT a Python package**  
(e.g., it’s just a script or notebook):

- **Do not use `-e .`**  
- Remove `-e .` from `requirements.txt`  
- You don’t need `setup.py` or `pyproject.toml` — plain `requirements.txt` is enough!

---

✅ **Summary**

| Case | Do you need `setup.py` or `pyproject.toml`? |
|----------------------------|-------------------------------|
| Using `-e .`               | ✅ Yes, required |
| Not using `-e .`           | ❌ No, not needed |

---





port :5000
us east-1  aws server


d