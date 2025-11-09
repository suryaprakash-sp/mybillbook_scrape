"""
Configuration file for MyBillBook scraper
Store your authentication credentials here
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# API Configuration
BASE_URL = "https://mybillbook.in/api/web"

# Authentication - You can either set these directly or use environment variables
# RECOMMENDED: Use .env file for security
AUTH_TOKEN = os.getenv("MYBILLBOOK_AUTH_TOKEN", "")
COOKIES = os.getenv("MYBILLBOOK_COOKIES", "")
COMPANY_ID = os.getenv("MYBILLBOOK_COMPANY_ID", "")

# If you prefer to set them directly (not recommended for production):
# AUTH_TOKEN = "Bearer eyJhbGciOiJIUzI1NiJ9..."
# COOKIES = "source_landing_url=https://mybillbook.in/; gbuuid=..."

# API Endpoints
ENDPOINTS = {
    "bulk_upload_status": "/bulk_upload/status",
    "items_stats": "/items/stats",
}

# Request Headers Template
def get_headers():
    """Returns headers for API requests"""
    return {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "authorization": AUTH_TOKEN,
        "client": "web",
        "company-id": COMPANY_ID,
        "content-type": "application/json",
        "cookie": COOKIES,
        "dnt": "1",
        "priority": "u=1, i",
        "referer": "https://mybillbook.in/app/home/items",
        "sec-ch-ua": '"Not_A Brand";v="99", "Chromium";v="142"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
    }

# Output Configuration
OUTPUT_DIR = "output"
OUTPUT_FILES = {
    "json": "inventory_complete.json",
    "detailed_json": "inventory_detailed.json",
    "csv": "inventory_export.csv",
}

# Scraping Configuration
REQUEST_TIMEOUT = 30  # seconds
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds between retries
