# App Catalog Automated Update System

## Overview

The JamfTerraform backend now includes an **automated App Catalog refresh system** that keeps the list of supported Jamf App Installer titles up-to-date without manual intervention.

## How It Works

### 1. **Weekly Automated Updates** (GitHub Actions)

A GitHub Actions workflow runs every Monday at 9am UTC to:

- Scrape the official Jamf Learning Hub for the latest App Catalog titles
- Compare against the current `backend/app_catalog.json`
- Auto-commit and push changes if new titles are detected
- Trigger Railway deploymentexecution via git push to `master`

**Workflow File**: `.github/workflows/update-catalog.yml`

### 2. **Hot Reload** (Backend)

The `LLMService` automatically detects when `app_catalog.json` is updated and reloads:

- Title list for validation
- System prompt injection for LLM semantic matching
- No backend restart required!

### 3. **Scraper Script**

**Location**: `scripts/update_app_catalog.py`

The scraper:

- Fetches HTML from Jamf Learning Hub
- Parses title list using BeautifulSoup
- Validates and deduplicates entries
- Updates JSON only if changes detected

## Manual Usage

### Trigger GitHub Actions Workflow

You can manually trigger the catalog update from GitHub:

1. Go to **Actions** tab in your repository
2. Select **"Update App Catalog"** workflow
3. Click **"Run workflow"** → **"Run workflow"**

### Run Scraper Locally

```bash
cd /Users/Shared/Tools/JamfTerraform
python3 scripts/update_app_catalog.py
```

**Exit codes**:

- `0`: Catalog was updated
- `1`: No changes detected
- `2`: Error occurred

### Test Hot Reload

Verify the hot-reload functionality works:

```bash
python3 scripts/test_hot_reload.py
```

This simulates updating the catalog and verifies the service detects and reloads it.

## Architecture Benefits

✅ **Zero Maintenance**: Catalog stays fresh automatically  
✅ **Audit Trail**: Git commits track when titles change  
✅ **No API Dependency**: Works around Jamf's lack of a public catalog API  
✅ **Auto-Deploy**: Railway redeploys on `master` branch updates  
✅ **Hot Reload**: Backend picks up changes without restart  
✅ **Fast Validation**: Local JSON lookup (no external calls during request handling)

## Files Added

- `.github/workflows/update-catalog.yml` - GitHub Actions workflow
- `scripts/update_app_catalog.py` - Web scraper
- `scripts/test_hot_reload.py` - Hot-reload test script

## Files Modified

- `backend/llm_service.py` - Added hot-reload logic with file modification tracking

## Future Improvements

If Jamf releases an official App Catalog API, the scraper can be easily swapped for an API client while keeping the rest of the architecture unchanged.

## Dependencies

The scraper requires:

- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `lxml` - Parser backend (optional, faster)

These are automatically installed in GitHub Actions and should be added to `backend/requirements.txt` if running locally.
