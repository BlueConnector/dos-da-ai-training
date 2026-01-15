import pandas as pd
from pathlib import Path
from typing import List, Optional
import asyncio
from playwright.async_api import TimeoutError

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
CONFIG_DIR = ROOT_DIR / "config"

async def first_match_text(element, selectors: List[str]) -> Optional[str]:
    """Try multiple selectors until one returns text."""
    for sel in selectors:
        try:
            child = await element.query_selector(sel)
            if child:
                text = await child.inner_text()
                if text and text.strip():
                    print(f"✅ Matched '{sel}'")
                    return " ".join(text.split())
        except:
            continue
    return None

async def first_match_attribute(element, selectors: List[str], attr: str) -> Optional[str]:
    """Try multiple selectors until one has the attribute."""
    for sel in selectors:
        try:
            child = await element.query_selector(sel)
            if child:
                value = await child.get_attribute(attr)
                if value:
                    print(f"✅ Attribute '{attr}' via '{sel}'")
                    return value
        except:
            continue
    return None

def ensure_output_dir() -> Path:
    (DATA_DIR / "sites_output").mkdir(exist_ok=True, parents=True)
    return DATA_DIR / "sites_output"

def save_dataframe(df: pd.DataFrame, filename: str):
    path = ensure_output_dir() / filename
    df.to_csv(path, index=False)
    print(f"💾 Saved {len(df)} rows → {path}")