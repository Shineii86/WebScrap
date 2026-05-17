# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly.

**Do NOT open a public issue.**

Instead, email the maintainer directly or use GitHub's private vulnerability reporting feature.

## Scope

This is a web scraping tool that runs in Google Colab. It does not:
- Store credentials or tokens
- Make outbound network requests (beyond the target URL)
- Execute arbitrary code from scraped pages
- Persist data beyond the Colab session

## Best Practices

- Only scrape websites you have permission to scrape
- Respect robots.txt and terms of service
- Do not use this tool for unauthorized data collection
- Be mindful of rate limiting and server load
