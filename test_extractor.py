import asyncio
from src.web_extractor import WebExtractor
from src.scrapers.playwright_scraper import ScraperConfig

async def test():
    config = ScraperConfig(headless=True)
    try:
        extractor = WebExtractor(model_name="alias-fast", scraper_config=config)
        print("WebExtractor initialized successfully!")

        # Test URL extraction
        from src.web_extractor import extract_url
        url = extract_url("Check out https://example.com")
        print(f"Extracted URL: {url}")
        assert url == "https://example.com"

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
