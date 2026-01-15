import asyncio
import pandas as pd
from pathlib import Path
import yaml
from .universal_scraper import scrape_site
from .utils import CONFIG_DIR

async def main():
    """Orchestrate ALL sites from CSV."""
    targets_df = pd.read_csv(CONFIG_DIR / "scraping_targets.csv")
    print(f"📋 Loaded {len(targets_df)} sites")
    
    all_data = []
    for _, row in targets_df.iterrows():
        site_config = row.to_dict()
        site_config["data_types"] = [t.strip() for t in str(row["data_types"]).split(",")]
        
        # Load site-specific YAML if exists
        if config_file := row.get("config_file"):
            yaml_path = CONFIG_DIR / config_file
            if yaml_path.exists():
                with open(yaml_path) as f:
                    site_config.update(yaml.safe_load(f))
        
        df = await scrape_site(site_config)
        all_data.append(df)
    
    # Master output
    combined = pd.concat(all_data, ignore_index=True)
    combined.to_csv("data/all_sites_summary.csv", index=False)
    print(f"✅ Combined {len(combined)} records from {len(all_data)} sites")

if __name__ == "__main__":
    asyncio.run(main())