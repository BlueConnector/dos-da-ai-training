import asyncio
import yaml
from typing import Dict, List, Any
import pandas as pd
from playwright.async_api import async_playwright, TimeoutError
from .utils import first_match_text, first_match_attribute, ensure_output_dir

async def scrape_site(site_config: Dict[str, Any]) -> pd.DataFrame:
    """Universal scraper: ANY site via YAML/CSV config."""
    site_name = site_config["site_name"]
    url = site_config["url"]
    
    print(f"🚀 [{site_name}] {url}")
    
    rows = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, timeout=site_config.get("timeout_ms", 10000))
            rows = await extract_products(page, site_config)
        finally:
            await browser.close()
    
    df = pd.DataFrame(rows)
    if not df.empty:
        df["site"] = site_name
        df["scrape_time"] = pd.Timestamp.now()
        save_dataframe(df, f"{site_name}.csv")
    
    return df

async def extract_products(page, config: Dict[str, Any]) -> List[Dict]:
    """Extract using 4-tier fallback strategy."""
    rows = []
    
    # Tier 1: Try configured card selectors
    card_selectors = config.get("product", {}).get("card_selectors", [".product-card"])
    cards = []
    
    for card_sel in card_selectors:
        cards = await page.query_selector_all(card_sel)
        if cards:
            print(f"✅ Found {len(cards)} cards via '{card_sel}'")
            break
    
    # Extract fields from each card
    field_configs = config.get("product", {}).get("fields", {})
    for i, card in enumerate(cards[:10]):  # Training limit
        row = {"card_index": i + 1}
        
        for field, fconfig in field_configs.items():
            if attr := fconfig.get("attribute"):
                row[field] = await first_match_attribute(card, fconfig["selectors"], attr)
            else:
                row[field] = await first_match_text(card, fconfig["selectors"])
        
        rows.append(row)
    
    return rows