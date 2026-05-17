# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] - 2026-05-17

### Added
- Initial release of WebScrap
- Full-page web scraper using Selenium + headless Chromium
- `notebook/WebScrap.ipynb` — 3-cell Colab notebook with inline-styled UI
- `src/config.py` — constants, Chrome options, UI theme tokens
- `src/scraper.py` — core scraping engine with auto-scroll, metadata extraction
- `src/ui.py` — theme-safe Colab UI components (cards, stats, tables)
- JavaScript-heavy site support (Next.js, React, Vue, Angular, Nuxt)
- Auto-scroll for lazy-loaded content
- Custom JavaScript execution after page load
- Configurable timeout and wait-after-load settings
- HTML preview with syntax highlighting
- Link extraction with text and resolved URLs
- Image extraction with alt text and dimensions
- Meta tag extraction (Open Graph, Twitter Cards, description, keywords)
- Metadata export as JSON alongside HTML
- ZIP download for all scraped files
- Content hash for deduplication
- Redirect detection and reporting
- Comprehensive README with architecture, badges, FAQ
- CHANGELOG.md — version history tracking
- CONTRIBUTING.md — contribution guidelines
- GUIDE.md — beginner-friendly user guide
- SECURITY.md — vulnerability reporting policy
- .github/ISSUE_TEMPLATE/ — bug report and feature request templates
- .github/PULL_REQUEST_TEMPLATE.md — PR checklist
- .gitignore — Python, Jupyter, output files, OS artifacts
- requirements.txt — core dependencies
- LICENSE — MIT license
