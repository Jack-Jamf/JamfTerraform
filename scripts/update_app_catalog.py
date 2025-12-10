"""
Automated scraper to update Jamf App Catalog titles.

This script fetches the latest list of App Installer titles from the Jamf Learning Hub
and updates backend/app_catalog.json if changes are detected.
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


class JamfAppCatalogScraper:
    """Scraper for Jamf App Catalog titles."""
    
    # Official Jamf Learning Hub page with App Installer titles
    CATALOG_URL = "https://learn.jamf.com/en-US/bundle/technical-articles/page/App_Installers_Software_Titles.html"
    
    # Fallback: GitHub-hosted mirror (if available)
    FALLBACK_URL = None
    
    def __init__(self, catalog_path: str = "backend/app_catalog.json"):
        """Initialize scraper with path to catalog JSON file."""
        self.catalog_path = Path(catalog_path)
    
    def fetch_titles_from_web(self) -> Optional[List[str]]:
        """
        Fetch app titles from the Jamf Learning Hub.
        
        Note: The Learning Hub page may require authentication or have rate limiting.
        This implementation attempts to parse the public-facing version.
        
        Returns:
            List of app titles if successful, None otherwise.
        """
        try:
            headers = {
                "User-Agent": "JamfTerraform-CatalogUpdater/1.0"
            }
            
            response = requests.get(self.CATALOG_URL, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Strategy 1: Look for table rows (common structure for such lists)
            titles = self._extract_from_table(soup)
            
            if not titles:
                # Strategy 2: Look for list items
                titles = self._extract_from_list(soup)
            
            if not titles:
                print("⚠️  Could not parse titles from HTML structure", file=sys.stderr)
                return None
            
            return titles
            
        except requests.RequestException as e:
            print(f"❌ Failed to fetch catalog page: {e}", file=sys.stderr)
            return None
    
    def _extract_from_table(self, soup: BeautifulSoup) -> List[str]:
        """Extract titles from HTML table structure."""
        titles = []
        
        # Look for tables that might contain app names
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                for cell in cells:
                    text = cell.get_text(strip=True)
                    # App titles typically don't contain URLs or HTML tags
                    if text and len(text) > 2 and not text.startswith('http'):
                        # Basic validation: app titles usually have letters and may include numbers
                        if re.match(r'^[A-Za-z0-9\s\-\.()]+$', text):
                            titles.append(text)
        
        return self._deduplicate_and_clean(titles)
    
    def _extract_from_list(self, soup: BeautifulSoup) -> List[str]:
        """Extract titles from HTML list structure (ul, ol)."""
        titles = []
        
        # Look for unordered or ordered lists
        lists = soup.find_all(['ul', 'ol'])
        for list_elem in lists:
            items = list_elem.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 2:
                    titles.append(text)
        
        return self._deduplicate_and_clean(titles)
    
    def _deduplicate_and_clean(self, titles: List[str]) -> List[str]:
        """Remove duplicates and clean up title strings."""
        # Remove duplicates while preserving order
        seen = set()
        unique_titles = []
        
        for title in titles:
            # Clean up whitespace
            title = ' '.join(title.split())
            
            if title and title not in seen:
                seen.add(title)
                unique_titles.append(title)
        
        return sorted(unique_titles)
    
    def load_current_catalog(self) -> List[str]:
        """Load the current catalog from JSON file."""
        try:
            with open(self.catalog_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Catalog file not found: {self.catalog_path}", file=sys.stderr)
            return []
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in catalog file: {e}", file=sys.stderr)
            return []
    
    def save_catalog(self, titles: List[str]) -> None:
        """Save titles to catalog JSON file."""
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.catalog_path, 'w') as f:
            json.dump(titles, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline
    
    def update_if_changed(self) -> bool:
        """
        Fetch latest titles and update catalog if changed.
        
        Returns:
            True if catalog was updated, False otherwise.
        """
        print("🔍 Fetching latest Jamf App Catalog titles...")
        
        new_titles = self.fetch_titles_from_web()
        
        if not new_titles:
            print("❌ Failed to fetch titles from web", file=sys.stderr)
            return False
        
        current_titles = self.load_current_catalog()
        
        # Compare as sets to detect any additions or removals
        new_set = set(new_titles)
        current_set = set(current_titles)
        
        if new_set == current_set:
            print(f"ℹ️  No changes detected ({len(current_titles)} titles)")
            return False
        
        # Calculate differences
        added = new_set - current_set
        removed = current_set - new_set
        
        print(f"\n📊 Changes detected:")
        print(f"   • Total titles: {len(new_titles)}")
        print(f"   • Added: {len(added)}")
        print(f"   • Removed: {len(removed)}")
        
        if added:
            print(f"\n   ➕ Added titles:")
            for title in sorted(added):
                print(f"      - {title}")
        
        if removed:
            print(f"\n   ➖ Removed titles:")
            for title in sorted(removed):
                print(f"      - {title}")
        
        # Save updated catalog
        self.save_catalog(new_titles)
        print(f"\n✅ Updated {self.catalog_path}")
        
        return True


def main():
    """Main entry point."""
    scraper = JamfAppCatalogScraper()
    
    try:
        updated = scraper.update_if_changed()
        sys.exit(0 if updated else 1)  # Exit 0 if updated, 1 if no changes
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
