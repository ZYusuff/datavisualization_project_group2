# Group 2 Data visualization project
# Git & GitHub Teamwork Guide 

### När man laddat ner nya paket - **uv pip freeze > requirements.txt**
den som installerar pushar upp till sin branch, sedan requester en pull till main 

- De andra kör **git pull origin main** 
- **pip venv**
- **uv pip install -r requirements.txt** för att ladda ner uppdaterad requirements

---

## 📌 Git Branching Basics
Branching allows multiple developers to work on different features simultaneously.

### **Create a New Branch**
```bash
git branch feature-branch-name  # Creates a new branch
```

OR create **and switch** to the new branch in one command:
```bash
git checkout -b feature-branch-name
```

### **List All Branches**
```bash
git branch  # Shows all local branches
```

### **Switch Between Branches**
```bash
git checkout main  # Switch to the main branch
git checkout feature-branch-name  # Switch to another branch
```

### **Delete a Branch**
```bash
git branch -d feature-branch-name  # Deletes a branch locally
```

---

## 🔄 Keeping Your Branch Updated
Always **pull the latest changes** before working:
```bash
git checkout main
git pull origin main  # Get the latest updates from the main branch
```

Then, **rebase or merge** changes into your branch:
```bash
git checkout feature-branch-name
git merge main  # Merges updates from main into your branch
```

---

## 📤 Pushing and Sharing Work
After making changes, push your branch to GitHub:
```bash
git add .  # Stage all changes
git commit -m "Added new feature"
git push origin feature-branch-name  # Push changes to GitHub
```

---

## 🔀 Creating a Pull Request (PR)
1. Go to your repository on **GitHub**.
2. Click **Pull Requests** → **New Pull Request**.
3. Select your branch and compare it with `main`.
4. Add a description and click **Create Pull Request**.
5. Request reviews from teammates.

---

## ✅ Merging & Cleaning Up
Once your PR is **approved & merged**, delete the branch:
```bash
git branch -d feature-branch-name  # Delete locally
git push origin --delete feature-branch-name  # Delete on GitHub
```