import os
import anthropic
import markdown as md_converter
from duckduckgo_search import DDGS


# ── 1. Set up the Anthropic client ──────────────────────────────────
client = anthropic.Anthropic()
# (It automatically reads your ANTHROPIC_API_KEY environment variable)


# ── 2. Define the web search tool ───────────────────────────────────
tools = [
    {
        "name": "web_search",
        "description": "Search the web for current information about a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up"
                }
            },
            "required": ["query"]
        }
    }
]


# ── 3. The search function that DuckDuckGo calls ─────────────────────
def search_web(query: str) -> str:
    """Search DuckDuckGo and return top 5 results as text."""
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        formatted = []
        for r in results:
            formatted.append(
                f"Title: {r['title']}\n"
                f"URL: {r['href']}\n"
                f"Summary: {r['body']}\n"
            )
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Search failed: {str(e)}"


# ── 4. The main agent loop ────────────────────────────────────────────
def run_agent(topic: str) -> str:
    """
    Runs the research agent.
    Claude will decide when to search and what to search for.
    The loop keeps going until Claude is done and returns the final report.
    """
    print(f"\n🔍 Starting research on: {topic}")
    print("Agent is thinking...\n")


    system_prompt = """You are a deep research agent that creates
competitor analysis reports. When given a topic, you MUST:
1. Search the web at least 3 times with different queries
   to gather comprehensive information
2. Write a structured Markdown report covering the top 3
   competitors/players with these sections for each:
   - **Positioning**: How they present themselves in the market
   - **Differentiation**: What makes them unique
   - **Impact**: Traction, users, revenue, achievements
   - **Market Sentiment**: How users/analysts talk about them
3. End with a 'Key Takeaways' section


Format the report with proper Markdown headings (#, ##, ###).
Be specific and data-driven wherever possible."""


    messages = [
        {
            "role": "user",
            "content": f"Research the competitive landscape for: {topic}. Write a detailed competitor analysis report."
        }
    ]


    # The agent loop — keeps running until Claude stops calling tools
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages
        )


        # If Claude is done, extract the final text and return
        if response.stop_reason == "end_turn":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return "No report generated."


        # If Claude wants to use a tool (search), run the search
        if response.stop_reason == "tool_use":
            messages.append({
                "role": "assistant",
                "content": response.content
            })


            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  🔎 Searching: {block.input['query']}")
                    result = search_web(block.input["query"])
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })


            messages.append({
                "role": "user",
                "content": tool_results
            })


# ── 5. Save the report as a webpage ──────────────────────────────────
def save_as_webpage(markdown_text: str, topic: str):
    """Converts the Markdown report to a clean HTML webpage."""
    html_body = md_converter.markdown(
        markdown_text,
        extensions=["tables", "fenced_code"]
    )


    html = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Competitor Analysis: {topic}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 800px;
                margin: 2rem auto; padding: 0 1rem; color: #1a1a1a;
                line-height: 1.7; }}
        h1 {{ color: #0F6E56; border-bottom: 2px solid #E1F5EE;
              padding-bottom: 8px; }}
        h2 {{ color: #185FA5; margin-top: 2rem; }}
        h3 {{ color: #444; }}
        strong {{ color: #0F6E56; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 2rem 0; }}
        ul {{ padding-left: 1.5rem; }}
        li {{ margin: 6px 0; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""


    filename = topic.lower().replace(' ', '-') + '-report.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


    print(f"\n✅ Report saved as: {filename}")
    print(f"   Open this file in your browser to view the webpage.")
    return filename


# ── 6. Main entry point ───────────────────────────────────────────────
if __name__ == '__main__':
    topic = input('Enter a topic to research (e.g. AI coding assistants): ')
    if not topic.strip():
        topic = 'AI coding assistants'


    report_markdown = run_agent(topic)


    print('\n' + '='*60)
    print('REPORT PREVIEW (first 500 characters):')
    print('='*60)
    print(report_markdown[:500] + '...')


    save_as_webpage(report_markdown, topic)

