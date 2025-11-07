"""
Main scraper for MyBillBook inventory data
"""

import json
import csv
import os
from typing import List, Dict, Any
from datetime import datetime

from auth import MyBillBookAPI
from models import InventoryItem, BulkUploadStatus
from config import OUTPUT_DIR, OUTPUT_FILES


class InventoryScraper:
    """Main class for scraping MyBillBook inventory"""

    def __init__(self):
        self.api = MyBillBookAPI()
        self.items: List[InventoryItem] = []
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f"Created output directory: {OUTPUT_DIR}")

    def fetch_inventory(self) -> bool:
        """
        Fetch all inventory items from MyBillBook

        Returns:
            True if successful, False otherwise
        """
        print("\n" + "=" * 60)
        print("MYBILLBOOK INVENTORY SCRAPER")
        print("=" * 60 + "\n")

        # Test connection first
        if not self.api.test_connection():
            return False

        print("\nFetching complete inventory data...")

        # Get all items from the items API
        response = self.api.get_all_items(per_page=500)

        if not response:
            print("Failed to fetch inventory data.")
            return False

        # Parse the response
        try:
            total_count = response.get('total_count', 0)
            inventory_items = response.get('inventory_items', [])

            print(f"Total items in system: {total_count}")
            print(f"Items fetched: {len(inventory_items)}")

            # Convert API response to our InventoryItem objects
            self.items = []
            for item_data in inventory_items:
                try:
                    # Map the new API structure to our existing model
                    mapped_item = {
                        'id': item_data.get('id'),
                        'name': item_data.get('name'),
                        'sku_code': item_data.get('sku_code', ''),
                        'category': item_data.get('item_category_name', ''),
                        'category_name': item_data.get('item_category_name', ''),
                        'item_category_id': item_data.get('item_category_id', ''),
                        'mrp': float(item_data.get('mrp') or 0),
                        'selling_price': float(item_data.get('selling_price') or 0),
                        'sales_price': float(item_data.get('sales_info', {}).get('price_per_unit') or 0),
                        'purchase_price': float(item_data.get('purchase_price') or 0),
                        'wholesale_price': float(item_data.get('wholesale_info', {}).get('price_per_unit') or 0) if item_data.get('wholesale_info', {}).get('price_per_unit') else None,
                        'wholesale_min_quantity': item_data.get('wholesale_min_quantity'),
                        'quantity': str(item_data.get('quantity', '0')),
                        'minimum_quantity': str(item_data.get('minimum_quantity', '0')),
                        'unit': item_data.get('unit', ''),
                        'unit_long': item_data.get('units', {}).get('primary_unit', item_data.get('unit', '')),
                        'gst_percentage': float(item_data.get('gst_percentage') or 0),
                        'sales_tax_included': item_data.get('is_tax_included', False),
                        'purchase_tax_included': item_data.get('purchase_info', {}).get('is_tax_included', False),
                        'description': item_data.get('description', ''),
                        'item_type': 0,  # Default value since API returns "good" as string
                        'show_on_store': False,  # Not in current API response
                        'excel_imported': False,  # Not in current API response
                        'created_at': item_data.get('created_at', ''),
                        'identification_code': item_data.get('identification_code', ''),
                        'conversion_factor': 0,  # Not in current API response
                        'additional_fields': item_data.get('additional_fields', []),
                        'sub_items': [],  # Not in current API response
                    }

                    item = InventoryItem.from_dict(mapped_item)
                    self.items.append(item)

                except Exception as e:
                    print(f"Warning: Failed to parse item {item_data.get('id', 'unknown')}: {e}")
                    continue

        except Exception as e:
            print(f"Error parsing response: {e}")
            return False

        print(f"\n[OK] Successfully fetched {len(self.items)} items!")
        return True

    def save_json(self, detailed: bool = False):
        """
        Save inventory data as JSON

        Args:
            detailed: If True, save with full details, else save compact version
        """
        filename = OUTPUT_FILES['detailed_json'] if detailed else OUTPUT_FILES['json']
        filepath = os.path.join(OUTPUT_DIR, filename)

        data = [item.to_dict() for item in self.items]

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Saved JSON: {filepath} ({len(self.items)} items)")

    def save_csv(self):
        """Save inventory data as CSV"""
        filepath = os.path.join(OUTPUT_DIR, OUTPUT_FILES['csv'])

        if not self.items:
            print("No items to save.")
            return

        # Get all field names from the first item
        fieldnames = [
            'id', 'name', 'sku_code', 'category', 'category_name',
            'mrp', 'selling_price', 'sales_price', 'purchase_price',
            'wholesale_price', 'wholesale_min_quantity',
            'quantity', 'minimum_quantity', 'unit', 'unit_long',
            'gst_percentage', 'sales_tax_included', 'purchase_tax_included',
            'description', 'item_type', 'show_on_store', 'excel_imported',
            'created_at', 'identification_code', 'conversion_factor',
            'item_category_id', 'index'
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for item in self.items:
                row = item.to_dict()
                # Remove complex fields that don't work well in CSV
                row.pop('additional_fields', None)
                row.pop('sub_items', None)
                writer.writerow(row)

        print(f"[OK] Saved CSV: {filepath} ({len(self.items)} items)")

    def print_summary(self):
        """Print a summary of the scraped inventory"""
        if not self.items:
            print("No items to summarize.")
            return

        print("\n" + "=" * 60)
        print("INVENTORY SUMMARY")
        print("=" * 60)

        # Total items
        print(f"\nTotal Items: {len(self.items)}")

        # Categories
        categories = {}
        for item in self.items:
            cat = item.category_name or item.category
            categories[cat] = categories.get(cat, 0) + 1

        print(f"\nCategories ({len(categories)}):")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {cat}: {count} items")

        # Price statistics
        prices = [item.selling_price for item in self.items if item.selling_price > 0]
        if prices:
            print(f"\nPrice Range:")
            print(f"  - Lowest: Rs.{min(prices):,.2f}")
            print(f"  - Highest: Rs.{max(prices):,.2f}")
            print(f"  - Average: Rs.{sum(prices)/len(prices):,.2f}")

        # Total inventory value
        total_value = sum(
            float(item.quantity) * item.selling_price
            for item in self.items
            if item.quantity and item.quantity != 'NaN'
        )
        print(f"\nTotal Inventory Value: Rs.{total_value:,.2f}")

        print("\n" + "=" * 60)

    def export_all(self):
        """Export inventory in all formats"""
        if not self.items:
            print("No items to export.")
            return

        print("\nExporting inventory data...")
        self.save_json(detailed=False)
        self.save_json(detailed=True)
        self.save_csv()
        print("\n[OK] All exports completed!")

    def run(self):
        """Main method to run the scraper"""
        # Fetch inventory
        if not self.fetch_inventory():
            print("\n[FAIL] Scraping failed. Please check your configuration and try again.")
            return False

        # Print summary
        self.print_summary()

        # Export data
        self.export_all()

        print("\n" + "=" * 60)
        print("SCRAPING COMPLETED SUCCESSFULLY!")
        print("=" * 60 + "\n")

        return True


def main():
    """Entry point for the scraper"""
    scraper = InventoryScraper()
    success = scraper.run()

    if not success:
        exit(1)


if __name__ == "__main__":
    main()
