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
                result = await self.web_extractor.process_query(
                    message,
                    conversation_history=conversation_history,
                    progress_callback=progress_placeholder.text
                )
            finally:
                progress_placeholder.empty()
            return result

        try:
            # Try to get existing loop or create new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(process_with_progress())
        finally:
            loop.close()