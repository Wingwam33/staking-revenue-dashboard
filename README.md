# $ME Staking Revenue Share Dashboard

A dashboard for visualizing and calculating revenue share distribution based on $ME token staking power.

## Features

- **Real-time Revenue Calculations**: Adjust monthly net revenue and revenue share percentages to see instant updates
- **Flexible Distribution**: Customize the split between stakers and token buyback (default 50/50)
- **Tier Analysis**: View revenue share projections for common staking power tiers (1K - 1M SP)
- **Cohort Analysis**: Understand distribution across staking power ranges with user counts and average revenue per user
- **Individual Staker Breakdown**: Searchable, sortable table of all stakers with pagination
- **Expiring Stake Tracking**: Automatically filters out stakes expiring in the upcoming month
- **One-Click Snapshots**: Update staking data directly from the ME Foundation API

## Quick Start

### Option 1: GitHub Pages (Recommended - Instant & Free)

1. Upload these files to your GitHub repository:
   - `staking-revenue-dashboard.html`
   - `staking-data.json` (snapshot data)
   - `README.md`

2. Enable GitHub Pages:
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`
   - Click Save

3. Share the URL:
   - `https://yourusername.github.io/your-repo-name/staking-revenue-dashboard.html`
   - No server needed - instant loading!

**To update data:**
- Run `python3 server.py` locally
- Click "Take Snapshot"
- Upload new `staking-data.json` to GitHub
- Site updates automatically

### Option 2: Run Locally (For development)

1. **Start the server:**
   ```bash
   python3 server.py
   ```

2. **Open the dashboard:**
   - Navigate to `http://localhost:8000/staking-revenue-dashboard.html`

3. **Take a snapshot:**
   - Click "📸 Take Snapshot" button to fetch the latest staking data
   - The page will automatically reload with updated data

## How It Works

### Revenue Calculation Formula

```
Total Revenue to Distribute = Net Revenue × Revenue Share %
Stakers Pool = Total Revenue × Stakers Split %
Buyback Pool = Total Revenue × Buyback Split %

Individual Share = (User's Staking Power / Total Staking Power) × Stakers Pool
```

### Expiring Stakes

Stakes that expire during the upcoming month (February 2026) are automatically excluded from all calculations. This ensures revenue share is only distributed to eligible stakers.

## Project Structure

- `staking-revenue-dashboard.html` - Main dashboard (single-page app)
- `server.py` - Python HTTP server with API endpoint for fetching snapshots
- `staking-data.json` - Cached snapshot of staking data (generated via API)

## API Integration

The dashboard fetches data from the ME Foundation staking API:
```
https://mefoundation.com/api/trpc/staking.getStakerSnapshot
```

The server handles SSL certificate issues and CORS, saving the data locally for fast access.

## Configuration

All parameters can be adjusted directly in the dashboard UI:

- **Monthly Net Revenue**: Expected monthly revenue ($)
- **Revenue Share %**: Percentage of revenue to distribute (default: 15%)
- **Stakers Split %**: Percentage going to stakers (default: 50%)
- **Buyback Split %**: Percentage going to token buyback (default: 50%)

## Technical Details

- Pure HTML/CSS/JavaScript dashboard (no build process required)
- Python 3 backend for API proxy and file serving
- Responsive design with Magic Eden theme
- Client-side pagination for 59K+ stakers
- Real-time updates on input changes

## Requirements

- Python 3.x
- Modern web browser
- Internet connection (for initial data fetch)

## License

This is an internal tool for Magic Eden revenue distribution planning.
