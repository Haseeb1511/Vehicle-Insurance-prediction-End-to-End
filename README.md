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




## ✅ Running on AWS EC2

```markdown
- **Port:** `5000`
- **Region:** `us-east-1`
```


## working project on AWS EC2

![image](./images/Screenshot%20(74).png)



## ✅ Option 1: Temporarily disable the workflow to stop CI/CD
```markdown
Best for: Keep your workflow file, but skip running it for now.

1️⃣ Go to your repository on GitHub

Example: https://github.com/your-username/your-repo

2️⃣ Click the Actions tab at the top (next to Code, Issues, Pull requests).

3️⃣ Find your workflow in the list (e.g., CI, Deploy to EC2, Docker Build, etc.).

4️⃣ Open the workflow details page — you’ll see runs, logs, and settings.

5️⃣ On the top right of the workflow page, you’ll see a ... menu or “Manage workflow” button.

```