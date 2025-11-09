# MyBillBook Inventory Scraper

A powerful, cross-platform Python scraper to extract complete inventory data from MyBillBook with advanced filtering and multiple export formats.

## ✨ Features

- 🚀 **Fast & Reliable** - Direct API integration, no browser automation needed
- 📊 **Multiple Export Formats** - JSON, CSV, and Excel with auto-formatted columns
- 🔍 **Advanced Filtering** - Filter by category, stock levels, price ranges
- 💻 **Cross-Platform** - Works on Windows, Mac, and Linux
- 🎨 **User-Friendly CLI** - Simple command-line interface with helpful options
- ⚡ **Easy Setup** - Automated setup scripts for all platforms

## Problem Statement

MyBillBook's built-in reports and downloads are limited. This scraper:
- Extracts **ALL** inventory items (not just recent uploads)
- Provides complete product details including pricing, quantities, categories, and metadata
- Offers flexible filtering and multiple export formats
- Works across all operating systems

## 🚀 Quick Start

> **📖 New to Mac?** See the [Complete macOS Setup Guide](MACOS_SETUP.md) with screenshots and detailed instructions!

### Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
1. Check Python installation
2. Create virtual environment
3. Install all dependencies
4. Create `.env` file from template

### Manual Setup

1. **Install Python 3.8+** (if not already installed)

2. **Clone or download this repository**

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure credentials:**
   - Copy `.env.example` to `.env`
   - Edit `.env` and add your MyBillBook credentials (see Configuration section)

## 📖 Configuration

### Getting Your Credentials

1. **Login to MyBillBook** in your browser
2. **Open Developer Tools** (F12)
3. **Go to Network tab** and filter by "Fetch/XHR"
4. **Navigate to inventory page** (`https://mybillbook.in/app/home/items`)
5. **Find a request** to `/api/web/` endpoints
6. **Copy the headers:**
   - `Authorization` header (Bearer token)
   - `Cookie` header
   - `Company-Id` header

7. **Paste into `.env` file:**
```env
MYBILLBOOK_AUTH_TOKEN=Bearer your_token_here
MYBILLBOOK_COOKIES=your_cookies_here
MYBILLBOOK_COMPANY_ID=your_company_id_here
```

## 💻 Usage

### Basic Usage

Run the scraper with default settings:
```bash
python scraper.py
```

### Advanced Usage (CLI)

The CLI provides powerful filtering and customization options:

```bash
# Show all options
python cli.py --help

# Export to Excel only
python cli.py --format excel

# Filter by category
python cli.py --category "Ear Rings"

# Filter by stock level (items with 10+ units)
python cli.py --min-stock 10

# Filter by price range
python cli.py --min-price 100 --max-price 500

# Combine filters
python cli.py --category "Chains" --min-stock 5 --format excel

# Custom output directory
python cli.py --output ./my_exports

# Quiet mode (minimal output)
python cli.py --quiet
```

## 📤 Export Formats

The scraper generates multiple formats:

- **`inventory_complete.json`** - Compact JSON with all items
- **`inventory_detailed.json`** - Full JSON with complete details
- **`inventory_export.csv`** - Flattened CSV for Excel/Sheets
- **`inventory_export.xlsx`** - Excel file with auto-formatted columns

## 🔍 Filtering Options

| Filter | Description | Example |
|--------|-------------|---------|
| `--category` | Filter by category name | `--category "Rings"` |
| `--min-stock` | Minimum quantity | `--min-stock 10` |
| `--max-stock` | Maximum quantity | `--max-stock 100` |
| `--min-price` | Minimum selling price | `--min-price 500` |
| `--max-price` | Maximum selling price | `--max-price 2000` |

## 📂 Project Structure

```
mybillbook_scrape/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script for Mac/Linux
├── setup.bat             # Setup script for Windows
├── .env.example          # Template for credentials
├── config.py             # Configuration management
├── scraper.py            # Main scraping logic
├── cli.py                # Command-line interface
├── auth.py               # API authentication
├── models.py             # Data models
└── output/               # Exported data files
```

## 🛠️ Technical Details

### How It Works

1. **Direct API Access** - Uses MyBillBook's internal API endpoints (same as the web app)
2. **Session Authentication** - Maintains authenticated session using Bearer tokens
3. **Efficient Data Fetching** - Fetches all items in a single request (up to 500 items)
4. **Smart Filtering** - Client-side filtering for instant results
5. **Multiple Export Formats** - Generates JSON, CSV, and Excel simultaneously

### Data Extracted

Each inventory item includes:
- Basic Info: ID, Name, SKU, Category
- Pricing: MRP, Selling Price, Purchase Price, Wholesale Price
- Stock: Quantity, Minimum Quantity, Unit
- Tax: GST Percentage, Tax Inclusion Flags
- Metadata: Description, Created Date, Additional Fields

### Requirements

- Python 3.8 or higher
- Internet connection (for API access)
- Valid MyBillBook credentials

## 🔒 Security & Privacy

- **No Data Storage** - Credentials are stored locally in `.env` (git-ignored)
- **Read-Only Access** - Only fetches data, never modifies your inventory
- **Secure Communication** - All requests use HTTPS
- **No External Services** - Data stays on your machine

## 🆘 Troubleshooting

### "Permission denied" or "403 Error"
- Your credentials may have expired
- Re-capture the credentials from browser DevTools
- Update `.env` with fresh tokens

### "No module named..." Error
- Run `pip install -r requirements.txt` again
- Make sure you're in the virtual environment

### Excel Export Not Working
- Ensure `pandas` and `openpyxl` are installed
- Run: `pip install pandas openpyxl`

### Setup Script Doesn't Run (Mac/Linux)
- Make it executable: `chmod +x setup.sh`
- Run with: `./setup.sh`

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is for educational and personal use. Please respect MyBillBook's terms of service.

## ✅ Status

**v1.0 - Fully Functional**

Successfully tested with:
- ✅ 235+ inventory items
- ✅ 14 product categories
- ✅ Cross-platform compatibility (Windows, Mac, Linux)
- ✅ All export formats working
- ✅ Advanced filtering operational

---

**Made with ❤️ for easier inventory management**