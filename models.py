"""
Data models for MyBillBook inventory items
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any
from datetime import datetime


@dataclass
class InventoryItem:
    """Represents a single inventory item from MyBillBook"""

    # Core Information
    id: str
    name: str
    sku_code: str
    category: str
    category_name: str
    item_category_id: str

    # Pricing
    mrp: float
    selling_price: float
    sales_price: float
    purchase_price: float
    wholesale_price: Optional[float]
    wholesale_min_quantity: Optional[float]

    # Inventory
    quantity: str
    minimum_quantity: str
    unit: str
    unit_long: str

    # Tax
    gst_percentage: float
    sales_tax_included: bool
    purchase_tax_included: bool

    # Additional Details
    description: str
    item_type: int
    show_on_store: bool
    excel_imported: bool
    created_at: str
    identification_code: str
    conversion_factor: float

    # Complex Fields
    additional_fields: List[Any] = field(default_factory=list)
    sub_items: List[Any] = field(default_factory=list)

    # Metadata
    index: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert the item to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'sku_code': self.sku_code,
            'category': self.category,
            'category_name': self.category_name,
            'item_category_id': self.item_category_id,
            'mrp': self.mrp,
            'selling_price': self.selling_price,
            'sales_price': self.sales_price,
            'purchase_price': self.purchase_price,
            'wholesale_price': self.wholesale_price,
            'wholesale_min_quantity': self.wholesale_min_quantity,
            'quantity': self.quantity,
            'minimum_quantity': self.minimum_quantity,
            'unit': self.unit,
            'unit_long': self.unit_long,
            'gst_percentage': self.gst_percentage,
            'sales_tax_included': self.sales_tax_included,
            'purchase_tax_included': self.purchase_tax_included,
            'description': self.description,
            'item_type': self.item_type,
            'show_on_store': self.show_on_store,
            'excel_imported': self.excel_imported,
            'created_at': self.created_at,
            'identification_code': self.identification_code,
            'conversion_factor': self.conversion_factor,
            'additional_fields': self.additional_fields,
            'sub_items': self.sub_items,
            'index': self.index,
        }

    @staticmethod
    def from_dict(data: dict) -> 'InventoryItem':
        """Create an InventoryItem from a dictionary"""
        return InventoryItem(
            id=data.get('id', ''),
            name=data.get('name', ''),
            sku_code=data.get('sku_code', ''),
            category=data.get('category', ''),
            category_name=data.get('category_name', ''),
            item_category_id=data.get('item_category_id', ''),
            mrp=data.get('mrp', 0),
            selling_price=data.get('selling_price', 0),
            sales_price=data.get('sales_price', 0),
            purchase_price=data.get('purchase_price', 0),
            wholesale_price=data.get('wholesale_price'),
            wholesale_min_quantity=data.get('wholesale_min_quantity'),
            quantity=str(data.get('quantity', '0')),
            minimum_quantity=str(data.get('minimum_quantity', '0')),
            unit=data.get('unit', ''),
            unit_long=data.get('unit_long', ''),
            gst_percentage=data.get('gst_percentage', 0),
            sales_tax_included=data.get('sales_tax_included', False),
            purchase_tax_included=data.get('purchase_tax_included', False),
            description=data.get('description', ''),
            item_type=data.get('item_type', 0),
            show_on_store=data.get('show_on_store', False),
            excel_imported=data.get('excel_imported', False),
            created_at=data.get('created_at', ''),
            identification_code=data.get('identification_code', ''),
            conversion_factor=data.get('conversion_factor', 0),
            additional_fields=data.get('additional_fields', []),
            sub_items=data.get('sub_items', []),
            index=data.get('index'),
        )


@dataclass
class BulkUploadStatus:
    """Represents the bulk upload status response structure"""

    id: str
    spreadsheet_id: str
    company_id: str
    upload_status: str
    upload_type: str
    success_items: List[InventoryItem] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict) -> 'BulkUploadStatus':
        """Create a BulkUploadStatus from API response"""
        success_data = data.get('meta', {}).get('success', [])
        success_items = [InventoryItem.from_dict(item) for item in success_data]

        return BulkUploadStatus(
            id=data.get('id', ''),
            spreadsheet_id=data.get('spreadsheet_id', ''),
            company_id=data.get('company_id', ''),
            upload_status=data.get('upload_status', ''),
            upload_type=data.get('upload_type', ''),
            success_items=success_items,
        )
