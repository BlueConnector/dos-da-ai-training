# DOS Data Analytics & AI Training – Web Extraction Lab 🎯

## 🚀 Quick Start (GitHub Codespaces)

1. Fork this repo → **Open in Codespaces**
2. Wait ~2 min for auto-setup (Playwright installs)
3. Run the universal scraper:

```bash
python -m src.process_multi_site

Output: data/sites_output/*.csv (one per site)



## For Statisticians (No Python Required)
### Add new sites
1. Edit config/scraping_targets.csv → add row
2. Create config/selectors_<site>.yaml → paste selectors from DevTools
3. Run: python -m src.process_multi_site

### Fix broken scrapers
1. Check logs → see which selector failed
2. Edit config/selectors_<site>.yaml → add fallback selector
3. Re-run scraper

## Architecture
config/scraping_targets.csv → universal_scraper.py → data/sites_output/*.csv
                           (statisticians own)      (engineers own)

## 🧪 Lab Exercises
Exercise 1: Simulate site redesign → fix via YAML fallbacks

Exercise 2: Add Cold Storage site → 90 seconds via CSV

Exercise 3: RedMart "selector drift" → YAML-only recovery

## 📊 Expected Output

data/sites_output/
├── redmart_groceries.csv     (47 items)
├── sample_store.csv          (6 items)  
├── ntuc_fairprice.csv        (24 items)
└── all_sites_summary.csv     (combined)



✅ Statisticians: edit CSV/YAML (no Python needed)
✅ Engineers: maintain ONE universal engine
✅ Scale: 5→50 sites = add CSV rows
✅ Resilience: 4-tier fallbacks built-in
✅ Audit: full logs + per-site CSVs
✅ Lab-ready: sample sites + "broken" versions for training


## Lab Workflow

# 1. Start Codespaces → auto-installs everything
$ python -m src.process_multi_site
📋 Scraping 3 sites...
✅ redmart: 47 items → data/sites_output/redmart.csv
✅ sample_store: 6 items → data/sites_output/sample_store.csv

# 2. Lab: simulate site change
$ # Edit scraping_targets.csv → point to products_v2.html
$ python -m src.process_multi_site
⚠️ sample_store: 0/6 names found (layout drift detected)

# 3. Fix via YAML only
$ # Edit config/selectors_sample.yaml → add fallbacks
$ python -m src.process_multi_site
✅ sample_store: 6/6 recovered via fallback selectors



dos-da-ai-training/
├── .devcontainer/
│   └── devcontainer.json                    # Codespaces config (Playwright ready)
├── config/
│   ├── scraping_targets.csv                  # MASTER: sites + data types (Excel!)
│   ├── selectors_redmart.yaml                # Site-specific selectors/fallbacks
│   ├── selectors_sample.yaml                 # Lab exercise selectors
│   └── selectors_ntuc.yaml                   # Example for competitor site
├── data/
│   ├── sample_prices.csv                     # Lab warm-up data
│   └── sites_output/                         # AUTO-GENERATED per-site CSVs
│       ├── redmart.csv
│       ├── sample_store.csv
│       └── ntuc_fairprice.csv
├── sample_site/
│   ├── products_v1.html                      # Original (works with default selectors)
│   └── products_v2.html                      # "Broken" version for lab (class changes)
├── src/
│   ├── __init__.py
│   ├── universal_scraper.py                  # CORE: 1 engine → ALL sites
│   ├── process_multi_site.py                 # Orchestrator: CSV → multi-site runs
│   ├── utils.py                              # Fallback helpers, parsing, logging
│   └── brittle_scraper.py                    # LAB: contrast with old approach
├── notebooks/
│   └── lab_overview.ipynb                    # Optional: Jupyter walkthrough
├── README.md                                 # Lab instructions + architecture
├── requirements.txt                          # pandas, playwright, pyyaml
└── .gitignore

