import asyncio
from src.utils.browser_tools import get_all_browser_tools

def test_tools():
    tools = get_all_browser_tools()
    print(f"Number of tools initialized: {len(tools)}")
    for tool in tools:
        print(f"Tool name: {tool.name}")

if __name__ == "__main__":
    test_tools()
