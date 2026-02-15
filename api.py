import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from src.web_extractor import WebExtractor
from src.scrapers.playwright_scraper import ScraperConfig

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str
    query: str
    model_name: Optional[str] = "alias-fast"

@app.get("/health")
async def health():
    return {"status": "ok", "message": "CyberScraper 2077 API is running"}

@app.post("/api/scrape")
async def scrape(request: ScrapeRequest):
    scraper_config = ScraperConfig(
        headless=True,
        max_retries=3,
        delay_after_load=5
    )

    extractor = WebExtractor(model_name=request.model_name, scraper_config=scraper_config)
    try:
        # Construct the query by combining URL and the specific request
        full_query = f"{request.url} {request.query}"
        response = await extractor.process_query(full_query)

        # If response is a tuple (csv/excel), extract the first part
        if isinstance(response, tuple):
            response = response[0]

        return {
            "url": request.url,
            "query": request.query,
            "response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
