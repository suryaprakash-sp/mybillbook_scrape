# MyBillBook Scraper - macOS Setup Guide

Complete step-by-step instructions for setting up and running the scraper on macOS.

---

## 📋 Prerequisites

Before you begin, ensure you have:
- macOS (any recent version)
- Internet connection
- MyBillBook account with active login

---

## 🚀 Step 1: Install Python

1. **Check if Python is already installed:**
   ```bash
   python3 --version
   ```

2. **If Python is not installed or version is below 3.8:**
   - Visit https://www.python.org/downloads/
   - Download Python 3.11 or later for macOS
   - Open the downloaded `.pkg` file
   - Follow the installation wizard
   - Click "Install" and enter your password when prompted

3. **Verify installation:**
   ```bash
   python3 --version
   # Should show: Python 3.11.x or higher
   ```

---

## 📥 Step 2: Download the Repository

### Option A: Using Git (Recommended)

1. **Install Git (if not already installed):**
   ```bash
   # Check if git is installed
   git --version

   # If not installed, macOS will prompt you to install Command Line Tools
   # Click "Install" when prompted
   ```

2. **Clone the repository:**
   ```bash
   # Navigate to where you want to save the project
   cd ~/Documents

   # Clone the repository
   git clone https://github.com/suryaprakash-sp/mybillbook_scrape.git

   # Enter the project directory
   cd mybillbook_scrape
   ```

### Option B: Download ZIP

1. Go to https://github.com/suryaprakash-sp/mybillbook_scrape
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your Documents folder
5. Open Terminal and navigate to the folder:
   ```bash
   cd ~/Documents/mybillbook_scrape-main
   ```

---

## 🛠️ Step 3: Open in VS Code

1. **Install VS Code (if not already installed):**
   - Visit https://code.visualstudio.com/
   - Download for macOS
   - Open the downloaded `.zip` file
   - Drag "Visual Studio Code" to Applications folder

2. **Open the project in VS Code:**
   ```bash
   # From the project directory
   code .
   ```

   *If the `code` command doesn't work:*
   - Open VS Code manually
   - Press `Cmd + Shift + P`
   - Type "shell command"
   - Select "Shell Command: Install 'code' command in PATH"
   - Restart Terminal and try again

---

## ⚙️ Step 4: Run Setup Script

1. **In VS Code, open the Terminal:**
   - Press `Ctrl + ` (backtick) OR
   - Menu: Terminal → New Terminal

2. **Make the setup script executable:**
   ```bash
   chmod +x setup.sh
   ```

3. **Run the setup script:**
   ```bash
   ./setup.sh
   ```

   The script will:
   - Check Python installation
   - Create a virtual environment
   - Install all required packages
   - Create a `.env` file for your credentials

4. **Wait for installation to complete** (may take 1-2 minutes)

---

## 🔑 Step 5: Get Your MyBillBook Credentials

1. **Open Safari (or any browser) and login to MyBillBook:**
   - Go to https://mybillbook.in
   - Login with your credentials

2. **Open Developer Tools:**
   - Press `Cmd + Option + I` OR
   - Right-click anywhere → "Inspect Element"

3. **Navigate to Network tab:**
   - Click the "Network" tab at the top
   - Click the filter icon and select "Fetch/XHR"

4. **Go to your inventory page:**
   - In MyBillBook, navigate to: https://mybillbook.in/app/home/items

5. **Find the API request:**
   - In the Network tab, look for requests containing `/api/web/`
   - Click on any request (e.g., one containing "items")

6. **Copy the credentials:**

   **a) Authorization Token:**
   - Click "Headers" tab
   - Scroll to "Request Headers"
   - Find "authorization:" and copy the ENTIRE value starting with "Bearer "
   - Example: `Bearer eyJhbGciOiJIUzI1NiJ9...` (very long string)

   **b) Cookies:**
   - In the same Request Headers section
   - Find "cookie:" and copy the ENTIRE value
   - Example: `source_landing_url=https://mybillbook.in/; gbuuid=...` (very long string)

   **c) Company ID:**
   - Find "company-id:" and copy the value
   - Example: `8fa87fa8-79e4-4a00-951d-7b9c3a41eefa`

---

## 📝 Step 6: Configure Credentials

1. **In VS Code, open the `.env` file:**
   - Click on `.env` in the file explorer (left sidebar)

2. **Paste your credentials:**
   ```env
   MYBILLBOOK_AUTH_TOKEN=Bearer paste_your_token_here
   MYBILLBOOK_COOKIES=paste_your_cookies_here
   MYBILLBOOK_COMPANY_ID=paste_your_company_id_here
   ```

3. **Save the file:**
   - Press `Cmd + S`

**Important:** Make sure there are NO spaces around the `=` sign and NO quotes around the values.

---

## ▶️ Step 7: Run the Scraper

1. **Activate the virtual environment (if not already active):**
   ```bash
   source venv/bin/activate
   ```

   You should see `(venv)` at the beginning of your terminal prompt.

2. **Run the basic scraper:**
   ```bash
   python scraper.py
   ```

   This will:
   - Connect to MyBillBook
   - Fetch all your inventory items
   - Show a summary
   - Export to JSON, CSV, and Excel formats

3. **Wait for completion** - You should see:
   ```
   ============================================================
   MYBILLBOOK INVENTORY SCRAPER
   ============================================================

   Testing API connection...
   [OK] Connection successful!

   Fetching complete inventory data...
   ...
   [OK] Successfully fetched XXX items!

   INVENTORY SUMMARY
   ...

   [OK] All exports completed!
   ```

---

## 📂 Step 8: Find Your Exported Files

1. **In VS Code:**
   - Look in the left sidebar (File Explorer)
   - Open the `output` folder

2. **You'll find these files:**
   - `inventory_complete.json` - All items in JSON format
   - `inventory_detailed.json` - Detailed JSON with full info
   - `inventory_export.csv` - **CSV file ready for Excel**
   - `inventory_export.xlsx` - **Excel file with formatting**

3. **Open the CSV in Excel:**
   ```bash
   # From terminal
   open output/inventory_export.csv
   ```

   Or:
   - Right-click `inventory_export.csv` in VS Code
   - Select "Reveal in Finder"
   - Double-click the file to open in Excel/Numbers

---

## 🎯 Advanced Usage (Optional)

### Filter by Category

Get only "Chains" items:
```bash
python cli.py --category "Chains" --format excel
```

### Filter by Stock Level

Get items with 10 or more units:
```bash
python cli.py --min-stock 10
```

### Filter by Price Range

Get items between Rs. 100 and Rs. 500:
```bash
python cli.py --min-price 100 --max-price 500
```

### Combine Filters

Get "Ear Rings" with stock >= 5, export to Excel only:
```bash
python cli.py --category "Ear Rings" --min-stock 5 --format excel
```

### See All Options

```bash
python cli.py --help
```

---

## 🔄 Running Again

**Next time you want to run the scraper:**

1. Open Terminal
2. Navigate to project folder:
   ```bash
   cd ~/Documents/mybillbook_scrape
   ```
3. Activate virtual environment:
   ```bash
   source venv/bin/activate
   ```
4. Run the scraper:
   ```bash
   python scraper.py
   ```

---

## ⚠️ Troubleshooting

### "Permission Denied" when running setup.sh
```bash
chmod +x setup.sh
./setup.sh
```

### "python3: command not found"
- Python is not installed or not in PATH
- Reinstall Python from python.org
- Make sure to check "Add Python to PATH" during installation

### "403 Error" or "Authentication Failed"
- Your credentials have expired
- Get fresh credentials from browser (Step 5)
- Update the `.env` file

### "No module named 'requests'" or similar
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Excel/CSV file shows garbled characters
- Open the CSV in Numbers (default macOS app)
- Or import into Excel: File → Import → Select CSV → UTF-8 encoding

---

## 🆘 Need Help?

1. **Check the main README.md** for more details
2. **Open an issue** on GitHub
3. **Check your credentials** - most issues are due to expired tokens

---

## ✅ Quick Checklist

- [ ] Python 3.8+ installed
- [ ] Repository downloaded
- [ ] Opened in VS Code
- [ ] Run `chmod +x setup.sh`
- [ ] Run `./setup.sh`
- [ ] Got credentials from browser DevTools
- [ ] Updated `.env` file
- [ ] Activated virtual environment (`source venv/bin/activate`)
- [ ] Run `python scraper.py`
- [ ] Found CSV file in `output` folder

---

**That's it! You're all set! 🎉**

Your inventory data is now in the `output` folder ready to use!
