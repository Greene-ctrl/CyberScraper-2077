import json
import logging
from typing import Optional, Dict, Any
from gradio_client import Client
from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Use the Hugging Face Space provided in the prompt
MCP_BROWSER_SPACE = "diamond-in/Browser-Use-mcp"

def get_browser_client():
    try:
        return Client(MCP_BROWSER_SPACE)
    except Exception as e:
        logger.error(f"Failed to initialize Gradio client: {e}")
        return None

@tool
def browse_and_extract(url: str, selector: str = "body", use_persistent: bool = False) -> str:
    """Browse to a URL and extract text content from the specified CSS selector."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            selector=selector,
            use_persistent=use_persistent,
            api_name="/browse_and_extract"
        )
        return str(result)
    except Exception as e:
        return f"Error during browse_and_extract: {str(e)}"

@tool
def click_element(url: str, selector: str, use_persistent: bool = False) -> str:
    """Click an element on the page identified by the CSS selector."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            selector=selector,
            use_persistent=use_persistent,
            api_name="/click"
        )
        return str(result)
    except Exception as e:
        return f"Error during click_element: {str(e)}"

@tool
def fill_field(url: str, selector: str, text: str, use_persistent: bool = False) -> str:
    """Fill a text field or form element identified by the CSS selector with the provided text."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            selector=selector,
            text=text,
            use_persistent=use_persistent,
            api_name="/fill"
        )
        return str(result)
    except Exception as e:
        return f"Error during fill_field: {str(e)}"

@tool
def execute_javascript(url: str, script: str, use_persistent: bool = False) -> str:
    """Execute custom JavaScript on the page and return the result."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            script=script,
            use_persistent=use_persistent,
            api_name="/execute_js"
        )
        return str(result)
    except Exception as e:
        return f"Error during execute_javascript: {str(e)}"

@tool
def get_cookies(url: str, use_persistent: bool = False) -> str:
    """Get all cookies for the current domain in JSON format."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            use_persistent=use_persistent,
            api_name="/get_cookies"
        )
        return str(result)
    except Exception as e:
        return f"Error during get_cookies: {str(e)}"

@tool
def set_cookies(url: str, cookies_json: str, use_persistent: bool = False) -> str:
    """Set cookies on the page from a JSON string."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            cookies_json=cookies_json,
            use_persistent=use_persistent,
            api_name="/set_cookies"
        )
        return str(result)
    except Exception as e:
        return f"Error during set_cookies: {str(e)}"

@tool
def scroll_page(url: str, direction: str = "bottom", pixels: float = 500, use_persistent: bool = False) -> str:
    """Scroll the page in a specified direction ('bottom', 'top', 'down', 'up')."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            direction=direction,
            pixels=pixels,
            use_persistent=use_persistent,
            api_name="/scroll_page"
        )
        return str(result)
    except Exception as e:
        return f"Error during scroll_page: {str(e)}"

@tool
def take_screenshot(url: str, full_page: bool = False, use_persistent: bool = False) -> str:
    """Take a screenshot of the current page and return the image data or path info."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            full_page=full_page,
            use_persistent=use_persistent,
            api_name="/screenshot"
        )
        return f"Screenshot captured: {json.dumps(result)}"
    except Exception as e:
        return f"Error during take_screenshot: {str(e)}"

@tool
def get_html_source(url: str, use_persistent: bool = False) -> str:
    """Get the full HTML source code of the current page."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            use_persistent=use_persistent,
            api_name="/get_html_source"
        )
        return str(result)
    except Exception as e:
        return f"Error during get_html_source: {str(e)}"

@tool
def get_page_info(url: str, use_persistent: bool = False) -> str:
    """Get comprehensive page information including title, URL, and interactive elements."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            use_persistent=use_persistent,
            api_name="/get_page_info"
        )
        return str(result)
    except Exception as e:
        return f"Error during get_page_info: {str(e)}"

@tool
def wait_for_element(url: str, selector: str, timeout: float = 10, use_persistent: bool = False) -> str:
    """Wait for an element matching the CSS selector to appear on the page."""
    client = get_browser_client()
    if not client: return "Error: Browser client unavailable."
    try:
        result = client.predict(
            url=url,
            selector=selector,
            timeout=timeout,
            use_persistent=use_persistent,
            api_name="/wait_for_element"
        )
        return str(result)
    except Exception as e:
        return f"Error during wait_for_element: {str(e)}"

@tool
def task_complete(reason: str) -> str:
    """Call this tool when you have successfully completed the task and have the final data or answer."""
    return f"TASK COMPLETE: {reason}"

@tool
def agent_reflection(thought: str, adaptation_plan: str) -> str:
    """Call this tool to reflect on your progress, especially after an error or unexpected result.
    Explain what you've learned and how you're adapting your strategy."""
    return f"REFLECTION: {thought}\nADAPTATION PLAN: {adaptation_plan}"

def get_all_browser_tools():
    """Returns a list of all browser automation tools."""
    return [
        browse_and_extract,
        click_element,
        fill_field,
        execute_javascript,
        get_cookies,
        set_cookies,
        scroll_page,
        take_screenshot,
        get_html_source,
        get_page_info,
        wait_for_element,
        task_complete,
        agent_reflection
    ]
