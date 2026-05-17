"""
WebScrap — Scraper engine.
Uses Selenium + headless Chromium to fully render any page (including SPAs).
"""

import os
import time
import json
import hashlib
from datetime import datetime, timezone
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from .config import (
    DEFAULT_TIMEOUT,
    DEFAULT_WAIT_AFTER_LOAD,
    CHROME_OPTIONS,
    USER_AGENT,
)

__all__ = [
    "scrape_url",
    "save_html",
    "save_metadata",
    "extract_text",
    "extract_links",
    "extract_images",
]


def _build_driver(
    chrome_bin: str | None = None,
    chromedriver_bin: str | None = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> webdriver.Chrome:
    """Create a headless Chrome WebDriver."""
    opts = Options()
    for arg in CHROME_OPTIONS:
        opts.add_argument(arg)
    if chrome_bin:
        opts.binary_location = chrome_bin

    service = Service(executable_path=chromedriver_bin) if chromedriver_bin else Service()
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_page_load_timeout(timeout)
    return driver


def scrape_url(
    url: str,
    timeout: int = DEFAULT_TIMEOUT,
    wait_after: int = DEFAULT_WAIT_AFTER_LOAD,
    scroll: bool = True,
    execute_js: str | None = None,
    chrome_bin: str | None = None,
    chromedriver_bin: str | None = None,
) -> dict:
    """
    Scrape a URL and return full rendered HTML + metadata.

    Returns dict with keys:
        url, final_url, title, html, char_count, link_count,
        image_count, meta_tags, headers, scraped_at, load_time_s,
        scroll_count, file_size_bytes, content_hash
    """
    start = time.time()
    driver = None

    try:
        driver = _build_driver(chrome_bin, chromedriver_bin, timeout)
        driver.get(url)

        # Wait for document ready
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Extra settle time for JS-heavy frameworks
        time.sleep(wait_after)

        # Scroll to trigger lazy-loaded content
        scroll_count = 0
        if scroll:
            scroll_count = _auto_scroll(driver)

        # Execute optional user JS
        if execute_js:
            try:
                driver.execute_script(execute_js)
                time.sleep(1)
            except Exception:
                pass

        # Grab the rendered HTML
        html = driver.page_source
        final_url = driver.current_url
        title = driver.title

        # Parse metadata
        soup = BeautifulSoup(html, "html.parser")

        meta_tags = {}
        for tag in soup.find_all("meta"):
            name = tag.get("name") or tag.get("property") or tag.get("http-equiv")
            content = tag.get("content")
            if name and content:
                meta_tags[name] = content

        links = soup.find_all("a", href=True)
        images = soup.find_all("img", src=True)

        # Response headers via requests fallback
        headers = {}
        try:
            import requests as req
            resp = req.head(url, timeout=10, allow_redirects=True, headers={"User-Agent": USER_AGENT})
            headers = dict(resp.headers)
        except Exception:
            pass

        load_time = round(time.time() - start, 2)
        content_hash = hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]

        return {
            "url": url,
            "final_url": final_url,
            "title": title,
            "html": html,
            "char_count": len(html),
            "link_count": len(links),
            "image_count": len(images),
            "meta_tags": meta_tags,
            "headers": headers,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "load_time_s": load_time,
            "scroll_count": scroll_count,
            "file_size_bytes": len(html.encode("utf-8")),
            "content_hash": content_hash,
        }

    finally:
        if driver:
            driver.quit()


def _auto_scroll(driver, max_scrolls: int = 50, pause: float = 0.8) -> int:
    """Scroll to bottom to trigger lazy-loading. Returns scroll count."""
    count = 0
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        count += 1
        if new_height == last_height:
            break
        last_height = new_height

    # Scroll back to top
    driver.execute_script("window.scrollTo(0, 0);")
    return count


def save_html(html: str, path: str) -> str:
    """Save HTML to file. Returns path."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def save_metadata(meta: dict, path: str) -> str:
    """Save metadata dict as JSON. Returns path."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    compact = {k: v for k, v in meta.items() if k != "html"}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(compact, f, indent=2, ensure_ascii=False)
    return path


def extract_text(html: str) -> str:
    """Extract readable text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator="\n", strip=True)


def extract_links(html: str, base_url: str = "") -> list[dict]:
    """Extract all links with text and resolved URLs."""
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if base_url and not href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            href = urljoin(base_url, href)
        links.append({
            "text": a.get_text(strip=True)[:120],
            "url": href,
        })
    return links


def extract_images(html: str, base_url: str = "") -> list[dict]:
    """Extract all images with src, alt, and dimensions."""
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img"):
        src = img.get("src", "")
        if base_url and src and not src.startswith(("data:", "http://", "https://")):
            src = urljoin(base_url, src)
        images.append({
            "src": src,
            "alt": img.get("alt", ""),
            "width": img.get("width"),
            "height": img.get("height"),
        })
    return images
