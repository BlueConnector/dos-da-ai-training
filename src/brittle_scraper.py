# LAB CONTRAST: Old "hard-coded" approach that breaks
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

def scrape_sample_brittle():
    """Breaks when .product-name → .product-title."""
    html = Path("sample_site/products_v1.html").read_text()
    soup = BeautifulSoup(html, "lxml")
    
    rows = []
    for card in soup.select(".product-card"):
        name = card.select_one(".product-name")  # HARDCODED → BREAKS
        price = card.select_one(".product-price")  # HARDCODED → BREAKS
        rows.append({"name": name.text if name else "", "price": price.text if price else ""})
    
    return pd.DataFrame(rows)

if __name__ == "__main__":
    print("🟡 Brittle scraper (for lab comparison):")
    print(scrape_sample_brittle())