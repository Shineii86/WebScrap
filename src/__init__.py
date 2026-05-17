"""WebScrap — Full-page web scraper for Google Colab."""

from .scraper import scrape_url, save_html, save_metadata, extract_text, extract_links, extract_images
from .config import DEFAULT_TIMEOUT, DEFAULT_WAIT_AFTER_LOAD, DEFAULT_OUTPUT_DIR
from .ui import show_ok, show_err, show_warn, show_info, show_step, show_header, show_stats, show_html_preview, show_links_table
