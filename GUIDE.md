# 📖 WebScrap User Guide

A beginner-friendly guide to using WebScrap in Google Colab.

## What is WebScrap?

WebScrap captures the **full rendered HTML** from any website — including pages built with JavaScript frameworks like React, Vue, Angular, and Next.js. Unlike simple HTTP requests, WebScrap runs a real browser to ensure all dynamic content is loaded before capture.

## Getting Started

### Step 1: Open the Notebook

1. Go to [Google Colab](https://colab.research.google.com)
2. Open `notebook/WebScrap.ipynb` from this repository
3. No GPU needed — this runs on CPU

### Step 2: Run Setup (Cell 1)

Click the **Play** button on the first cell. This installs:
- Chromium browser (headless)
- Selenium WebDriver
- BeautifulSoup HTML parser

This takes about 60 seconds on first run.

### Step 3: Scrape a Website (Cell 2)

1. Paste a URL into the `url` field
2. Adjust settings if needed (see below)
3. Run the cell

You'll see:
- Real-time progress updates
- Page statistics (size, links, images, load time)
- HTML preview
- Link table
- Key meta tags

### Step 4: Download (Cell 3)

Run the export cell to download all scraped files as a ZIP.

## Settings Guide

### Timeout (default: 30s)
How long to wait for the page to load. Increase for:
- Slow servers → 60s
- Heavy SPAs → 90–120s

### Wait After Load (default: 3s)
Extra time for JavaScript to finish executing after the page reports "complete." Increase for:
- Next.js / Nuxt apps → 5–8s
- Pages with delayed animations → 8–10s

### Auto-Scroll (default: on)
Scrolls to the bottom of the page to trigger lazy-loaded content (images, infinite scroll). Disable if you only need above-the-fold content.

### Custom JavaScript
Execute JavaScript after the page loads. Useful for:
- Clicking expand buttons: `document.querySelector('.expand').click()`
- Waiting for specific elements: (use with care)
- Triggering lazy loaders manually

## Common Use Cases

### Scraping a React/Next.js App
```
timeout: 60
wait_after_load: 8
auto_scroll: True
```

### Scraping a Static Blog
```
timeout: 15
wait_after_load: 1
auto_scroll: True
```

### Scraping a Heavy Media Site
```
timeout: 90
wait_after_load: 5
auto_scroll: True
```

## Output Files

For each scrape, you get:
- `domain_timestamp.html` — full rendered HTML
- `domain_timestamp_meta.json` — metadata (title, tags, stats, links)

## Limitations

- **No authentication:** Can't log into sites
- **No file downloads:** Only captures HTML (not PDFs, videos, etc.)
- **Single page:** Each run captures one URL
- **Colab session limits:** Very long sessions may timeout

## Need Help?

- Check the [FAQ](README.md#-faq) in the README
- Read the [Changelog](CHANGELOG.md) for known issues and fixes
- Review [SECURITY.md](SECURITY.md) for responsible usage
- Open an [issue](https://github.com/Shineii86/WebScrap/issues)
