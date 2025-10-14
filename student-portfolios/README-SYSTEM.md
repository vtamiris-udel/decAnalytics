# 🚀 Portfolio README Generation System

This folder contains an automated system that generates and maintains a comprehensive README.md file for all student portfolios.

## 📁 Files

- **`generate_portfolio_readme.py`** - Main Python script that scans student folders and generates the README
- **`test_generator.py`** - Test script to verify the generator works correctly
- **`requirements.txt`** - Python dependencies (currently none - uses only standard library)
- **`README.md`** - **AUTO-GENERATED** - Main portfolio index (do not edit manually!)
- **`README-SYSTEM.md`** - This file explaining the system

## 🔄 How It Works

1. **Automatic Trigger**: GitHub Actions monitors for changes to any `README.md` file in the `student-portfolios` folder or its subfolders
2. **Generation**: When changes are detected, the script automatically runs and:
   - Scans all student subfolders
   - Reads each student's `README.md` file
   - Extracts key information (nickname, interesting facts)
   - Generates a comprehensive index table
   - Updates the main `README.md` file
3. **Commit**: Changes are automatically committed and pushed back to the repository

## 🎯 What Gets Generated

The script creates a `README.md` with:
- **Student Table**: Name, nickname, interesting facts, and portfolio links
- **Instructions**: How new students can add their portfolios
- **Auto-update notice**: Information about the automated system
- **Last updated timestamp**: When the README was last generated

## 🧪 Testing Locally

To test the generator script locally:

```bash
# Navigate to student-portfolios folder
cd student-portfolios

# Run the generator
python generate_portfolio_readme.py

# Or run the test script
python test_generator.py
```

## 📝 Student README Format

Each student's `README.md` should follow this format for proper parsing:

```markdown
# 👨‍🎓 Student Portfolio - Your Name

---

## 📋 Student Information

| **Field** | **Details** |
|-----------|-------------|
| **Nickname/Pseudonym** | Your Nickname |
| **Interesting Fact** | An interesting fact about you |
| **Interesting Fact2** | Another interesting fact about you |

---

## 🖼️ Portfolio Images

### Image Title
![Description](image_filename.jpg)
```

## ⚠️ Important Notes

- **DO NOT manually edit** the main `README.md` file - it will be overwritten
- **DO edit** your individual student `README.md` files
- The system automatically detects new students when they add their folders
- All changes are logged in the GitHub Actions history

## 🐛 Troubleshooting

If the GitHub Action fails:
1. Check the Actions tab in your repository
2. Verify the Python script syntax is correct
3. Ensure student README files follow the expected format
4. Check that the `.github/workflows/update-portfolio-readme.yml` file exists

## 🔧 Customization

To modify the generated README format:
1. Edit the `generate_portfolio_readme.py` script
2. Update the `generate_portfolio_readme()` function
3. Test locally with `python test_generator.py`
4. Commit and push changes

## 📚 Dependencies

- **Python 3.7+** (uses only standard library)
- **Git** (for version control and GitHub Actions)
- **GitHub Actions** (for automation)

---

*This system automatically maintains an up-to-date index of all student portfolios!*
