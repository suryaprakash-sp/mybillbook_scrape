# MyBillBook Inventory Scraper

A Python-based scraper to extract complete inventory data from MyBillBook, overcoming the limitations of the built-in export/report features.

## Problem Statement

MyBillBook's built-in reports and downloads are limited, even when all categories are uploaded. This scraper extracts complete inventory data by:
1. Fetching all items from the inventory page (with item IDs and basic details)
2. Iterating through each item to fetch detailed information from individual item pages

## How It Works

1. **Authentication**: Uses provided session credentials to authenticate
2. **Inventory List Extraction**: Scrapes the inventory page to get all item IDs and basic details
3. **Detailed Item Extraction**: Loops through each item ID to fetch complete details from individual item pages
4. **Data Export**: Saves the complete inventory data in a structured format (CSV/JSON)

## Project Structure

```
mybillbook_scrape/
├── README.md
├── requirements.txt
├── config.py              # Configuration and credentials
├── scraper.py            # Main scraping logic
├── auth.py               # Authentication handling
├── models.py             # Data models for items
└── output/               # Exported data files
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure authentication (see Configuration section)

3. Run the scraper:
```bash
python scraper.py
```

## Configuration

Authentication credentials will need to be provided (cookies/tokens from an authenticated session).

## Output

The scraper generates:
- `inventory_list.json` - Complete list of all items with basic details
- `inventory_detailed.json` - Detailed information for each item
- `inventory_export.csv` - Flattened CSV for easy analysis

## Technical Approach

MyBillBook is a single-page application (SPA) that uses API endpoints to load data. The scraper:
- Identifies and uses the same API endpoints the web app uses
- Maintains session authentication
- Handles pagination for large inventories
- Respects rate limits to avoid overwhelming the server

## Status

✅ **COMPLETED** - Fully functional and tested with 254 items

## Results

Successfully scrapes and exports:
- **254 items** from MyBillBook inventory
- **14 categories** (Ear Rings, Chains, Bracelets, Rings, etc.)
- Complete pricing, quantities, and metadata
- Exports to JSON and CSV formats

## Verification

Stock analysis:
- 5 items with negative stock (-8 total)
- 58 items with zero stock
- 191 items with positive stock (3929 total)
- **Total: 254 items, 3921 units**