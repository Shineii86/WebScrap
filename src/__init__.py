"""WebScrap — Full-page web scraper for Google Colab."""

from .scraper import (
    scrape_url,
    save_html,
    save_metadata,
    extract_text,
    extract_links,
    extract_images,
)
from .config import DEFAULT_TIMEOUT, DEFAULT_WAIT_AFTER_LOAD, DEFAULT_OUTPUT_DIR, USER_AGENT
from .ui import (
    show_header,
    show_ok,
    show_warn,
    show_err,
    show_info,
    show_step,
    show_stats,
    show_html_preview,
    show_links_table,
    show_meta_tags,
)

__all__ = [
    # Scraper
    "scrape_url",
    "save_html",
    "save_metadata",
    "extract_text",
    "extract_links",
    "extract_images",
    # Config
    "DEFAULT_TIMEOUT",
    "DEFAULT_WAIT_AFTER_LOAD",
    "DEFAULT_OUTPUT_DIR",
    "USER_AGENT",
    # UI
    "show_header",
    "show_ok",
    "show_warn",
    "show_err",
    "show_info",
    "show_step",
    "show_stats",
    "show_html_preview",
    "show_links_table",
    "show_meta_tags",
]
