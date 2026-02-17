import asyncio
import streamlit as st
from src.web_extractor import WebExtractor
from src.scrapers.playwright_scraper import ScraperConfig
import os

class StreamlitWebScraperChat:
    def __init__(self, model_name, scraper_config: ScraperConfig = None):
        self.web_extractor = WebExtractor(model_name=model_name, scraper_config=scraper_config)

    def process_message(self, message: str, conversation_history: list[dict] | None = None) -> str:
        async def process_with_progress():
            progress_placeholder = st.empty()
            progress_placeholder.text("Processing...")
            try:
                # Ensure the web_extractor's scraper is closed and re-initialized if needed
                # to avoid loop-mismatch errors
                if hasattr(self.web_extractor, 'playwright_scraper'):
                    await self.web_extractor.playwright_scraper.close()

                result = await self.web_extractor.process_query(
                    message,
                    conversation_history=conversation_history,
                    progress_callback=progress_placeholder.text
                )
            finally:
                progress_placeholder.empty()
            return result

        # Use asyncio.run for clean loop management in each request
        # This avoids "Event loop is closed" errors by creating and destroying
        # a loop per process_message call.
        return asyncio.run(process_with_progress())