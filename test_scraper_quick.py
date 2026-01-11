#!/usr/bin/env python3
"""Quick test of the scraper to debug the issue"""

import sys
sys.path.insert(0, '/Users/zishine/VSCODE/deltahacks/deltahacks26/backend')

from scraper import scrape_realtor_ca_listing

# Test with the same URL from the integration guide
test_url = "https://www.realtor.ca/real-estate/29140184/2-prince-adam-court-king-king-city-king-city"

print("=" * 70)
print("Testing Realtor.ca scraper...")
print("=" * 70)
print(f"\nURL: {test_url}\n")

try:
    result = scrape_realtor_ca_listing(test_url)

    if "error" in result:
        print(f"❌ ERROR: {result['error']}")
    else:
        print(f"✓ Found {len(result.get('property_photos', []))} photos")
        print(f"✓ Address: {result.get('basic_info', {}).get('address', 'N/A')}")
        print(f"✓ Price: {result.get('basic_info', {}).get('price', 'N/A')}")

        if len(result.get('property_photos', [])) == 0:
            print("\n⚠️  WARNING: No photos found!")
            print("This might be due to:")
            print("  1. Robot check blocking the scraper")
            print("  2. Listing expired or removed")
            print("  3. Page structure changed")
        else:
            print("\n✓ Scraper is working correctly!")

except Exception as e:
    print(f"❌ EXCEPTION: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
