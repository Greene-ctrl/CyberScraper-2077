from src.utils.browser_tools import get_all_browser_tools
tools = get_all_browser_tools()
print([t.name for t in tools])
