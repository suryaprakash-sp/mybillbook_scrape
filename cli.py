"""
Enhanced command-line interface for MyBillBook scraper
"""

import argparse
import sys
import os

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    HAS_COLOR = False
    # Fallback for systems without colorama
    class Fore:
        CYAN = RED = GREEN = YELLOW = ''
    class Style:
        RESET_ALL = ''

from scraper import InventoryScraper


def print_banner():
    """Print application banner"""
    if HAS_COLOR:
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║          MyBillBook Inventory Scraper v1.0                ║
║          Extract complete inventory data easily           ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    else:
        banner = """
===============================================================
          MyBillBook Inventory Scraper v1.0
          Extract complete inventory data easily
===============================================================
"""
    print(banner)


def check_credentials():
    """Check if credentials are configured"""
    if not os.path.exists('.env'):
        if HAS_COLOR:
            print(f"{Fore.YELLOW}⚠ Warning: .env file not found!{Style.RESET_ALL}")
        else:
            print("Warning: .env file not found!")

        print(f"\nPlease create a .env file with your credentials:")
        print(f"  1. Copy .env.example to .env")
        print(f"  2. Fill in your authentication details")
        print(f"\nSee README.md for detailed instructions.\n")
        return False
    return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='MyBillBook Inventory Scraper - Extract complete inventory data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py                          # Run with default settings
  python cli.py --format excel           # Export to Excel only
  python cli.py --category "Ear Rings"   # Filter by category
  python cli.py --min-stock 10           # Filter items with stock >= 10
  python cli.py --output ./exports       # Custom output directory
  python cli.py --quiet                  # Minimal output
        """
    )

    parser.add_argument(
        '--format',
        choices=['all', 'json', 'csv', 'excel'],
        default='all',
        help='Export format (default: all)'
    )

    parser.add_argument(
        '--output',
        '-o',
        default='output',
        help='Output directory (default: output)'
    )

    parser.add_argument(
        '--category',
        '-c',
        help='Filter by category name'
    )

    parser.add_argument(
        '--min-stock',
        type=float,
        help='Filter items with stock >= this value'
    )

    parser.add_argument(
        '--max-stock',
        type=float,
        help='Filter items with stock <= this value'
    )

    parser.add_argument(
        '--min-price',
        type=float,
        help='Filter items with price >= this value'
    )

    parser.add_argument(
        '--max-price',
        type=float,
        help='Filter items with price <= this value'
    )

    parser.add_argument(
        '--no-summary',
        action='store_true',
        help='Skip printing summary'
    )

    parser.add_argument(
        '--quiet',
        '-q',
        action='store_true',
        help='Minimal output'
    )

    args = parser.parse_args()

    # Print banner unless quiet mode
    if not args.quiet:
        print_banner()

    # Check credentials
    if not check_credentials():
        sys.exit(1)

    # Create scraper instance
    scraper = InventoryScraper(output_dir=args.output, quiet=args.quiet)

    # Fetch inventory
    if not scraper.fetch_inventory():
        if HAS_COLOR:
            print(f"{Fore.RED}✗ Failed to fetch inventory{Style.RESET_ALL}")
        else:
            print("Failed to fetch inventory")
        sys.exit(1)

    # Apply filters
    if any([args.category, args.min_stock, args.max_stock, args.min_price, args.max_price]):
        scraper.apply_filters(
            category=args.category,
            min_stock=args.min_stock,
            max_stock=args.max_stock,
            min_price=args.min_price,
            max_price=args.max_price
        )

    # Print summary
    if not args.no_summary and not args.quiet:
        scraper.print_summary()

    # Export data
    if args.format == 'all':
        scraper.export_all()
    elif args.format == 'json':
        scraper.save_json()
        scraper.save_json(detailed=True)
    elif args.format == 'csv':
        scraper.save_csv()
    elif args.format == 'excel':
        scraper.save_excel()

    if not args.quiet:
        if HAS_COLOR:
            print(f"\n{Fore.GREEN}✓ Success! Data exported to {args.output}/{Style.RESET_ALL}\n")
        else:
            print(f"\nSuccess! Data exported to {args.output}/\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if HAS_COLOR:
            print(f"\n{Fore.YELLOW}⚠ Operation cancelled by user{Style.RESET_ALL}")
        else:
            print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        if HAS_COLOR:
            print(f"\n{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
        else:
            print(f"\n[ERROR] {e}")
        sys.exit(1)
