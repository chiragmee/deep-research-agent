import streamlit as st
import anthropic
from duckduckgo_search import DDGS
import markdown as md_converter
import time

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  .hero {
    background: linear-gradient(135deg, #0F6E56 0%, #185FA5 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
  }
  .hero h1 {
    color: white;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 0 0.5rem 0;
  }
  .hero p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0;
  }
  .badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: white;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.75rem 4px 0;
  }

  .built-by {
    text-align: center;
    color: #888;
    font-size: 0.8rem;
    margin-bottom: 1.5rem;
  }
  .built-by span {
    color: #0F6E56;
    font-weight: 600;
  }

  .section-card {
    background: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
  }
  .section-card h3 {
    color: #185FA5;
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    font-weight: 600;
  }

  .report-container {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 12px;
    padding: 2rem;
    margin-top: 1.5rem;
  }

  .search-log {
    background: #1e1e1e;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #9FE1CB;
    margin: 0.5rem 0;
  }

  .metric-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1.5rem;
  }
  .metric {
    flex: 1;
    background: #f0faf6;
    border: 1px solid #9FE1CB;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
  }
  .metric .num { font-size: 1.5rem; font-weight: 700; color: #0F6E56; }
  .metric .lbl { font-size: 0.75rem; color: #555; margin-top: 2px; }

  .stButton > button {
    background: linear-gradient(135deg, #0F6E56, #185FA5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
  }
  .stButton > button:hover { opacity: 0.9 !important; }

  .download-btn {
    display: inline-block;
    background: #0F6E56;
    color: white;
    border-radius: 8px;
    padding: 8px 20px;
    font-size: 0.85rem;
    font-weight: 600;
    text-decoration: none;
    margin-top: 1rem;
  }

  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Hero Section ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>🔍 Deep Research Agent</h1>
  <p>Enter any topic and get an AI-powered competitor analysis report in seconds</p>
  <span class="badge">⚡ Powered by Claude AI</span>
  <span class="badge">🌐 Live Web Search</span>
  <span class="badge">📊 Structured Reports</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="built-by">Built by <span>Chirag Mewara</span> · Deep Research Agent v1.0</div>
""", unsafe_allow_html=True)

# ── How it works ───────────────────────────────────────────────────────────────
with st.expander("ℹ️ How does this work?"):
    st.markdown("""
    This is an **AI Agent** — not just a chatbot. Here's what happens when you click Research:

    1. **Claude AI** decides what to search for based on your topic
    2. It calls the **DuckDuckGo search tool** multiple times to gather live web data
    3. It reads and synthesises all the results
    4. It writes a structured **competitor analysis report** covering:
       - 🎯 Positioning · 💡 Differentiation · 📈 Impact · 💬 Market Sentiment
    5. The report is displayed here and available to download as HTML
    """)

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown("### Enter your research topic")

col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "",
        placeholder="e.g. AI coding assistants, CRM software, no-code app builders...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)

# Example chips
st.markdown("**Quick examples:**")
ex_cols = st.columns(4)
examples = ["AI writing tools", "No-code builders", "CRM software", "Product analytics"]
for i, ex in enumerate(examples):
    with ex_cols[i]:
        if st.button(ex, key=f"ex_{i}"):
            topic = ex

# ── API Key input ──────────────────────────────────────────────────────────────
st.markdown("### 🔑 Your Anthropic API Key")
api_key = st.text_input(
    "",
    type="password",
    placeholder="sk-ant-api03-...",
    help="Get your key at console.anthropic.com",
    label_visibility="collapsed"
)
st.caption("🔒 Your key is never stored — it is only used for this session. Get one at [console.anthropic.com](https://console.anthropic.com)")

# ── Agent functions ────────────────────────────────────────────────────────────
def search_web(query: str) -> str:
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        formatted = []
        for r in results:
            formatted.append(f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}")
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Search failed: {str(e)}"

def run_agent(topic: str, api_key: str, log_container, progress_bar):
    client = anthropic.Anthropic(api_key=api_key)

    tools = [{
        "name": "web_search",
        "description": "Search the web for current information about a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    }]

    system_prompt = """You are a deep research agent that creates competitor analysis reports.
When given a topic, you MUST:
1. Search the web at least 3 times with different queries to gather comprehensive information
2. Write a structured Markdown report covering the top 3 competitors/players with these sections for each:
   - **Positioning**: How they present themselves in the market
   - **Differentiation**: What makes them unique
   - **Impact**: Traction, users, revenue, achievements
   - **Market Sentiment**: How users/analysts talk about them
3. End with a '## Key Takeaways' section with 3-4 bullet points

Format with proper Markdown headings. Be specific and data-driven."""

    messages = [{"role": "user", "content": f"Research the competitive landscape for: {topic}. Write a detailed competitor analysis report."}]

    searches_done = 0
    log_lines = []
    progress_bar.progress(10)

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            progress_bar.progress(100)
            for block in response.content:
                if block.type == "text":
                    return block.text, searches_done
            return "No report generated.", searches_done

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    searches_done += 1
                    query = block.input['query']
                    log_lines.append(f"🔎 Search {searches_done}: {query}")
                    log_container.markdown(
                        '<div class="search-log">' + '<br>'.join(log_lines) + '</div>',
                        unsafe_allow_html=True
                    )
                    progress_bar.progress(min(10 + searches_done * 20, 85))
                    result = search_web(query)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})

# ── Run Button ─────────────────────────────────────────────────────────────────
run_clicked = st.button("🚀 Research this topic")

if run_clicked:
    if not topic:
        st.warning("Please enter a topic first.")
    elif not api_key:
        st.warning("Please enter your Anthropic API key in the sidebar (click > on the left).")
    else:
        st.divider()
        st.markdown("### 🤖 Agent is working...")

        progress = st.progress(0)
        log_box = st.empty()
        status = st.empty()

        try:
            start = time.time()
            report, num_searches = run_agent(topic, api_key, log_box, progress)
            elapsed = round(time.time() - start, 1)

            status.success(f"✅ Report generated in {elapsed} seconds using {num_searches} web searches!")

            # Metrics
            word_count = len(report.split())
            st.markdown(f"""
            <div class="metric-row">
              <div class="metric"><div class="num">{num_searches}</div><div class="lbl">Web searches</div></div>
              <div class="metric"><div class="num">{word_count}</div><div class="lbl">Words in report</div></div>
              <div class="metric"><div class="num">{elapsed}s</div><div class="lbl">Time taken</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Report display
            st.markdown("### 📊 Your Competitor Analysis Report")
            st.markdown('<div class="report-container">', unsafe_allow_html=True)
            st.markdown(report)
            st.markdown('</div>', unsafe_allow_html=True)

            # Download button
            html_report = f"""<!DOCTYPE html>
<html><head><meta charset='UTF-8'><title>Competitor Analysis: {topic}</title>
<style>
  body{{font-family:-apple-system,sans-serif;max-width:800px;margin:2rem auto;padding:0 1rem;color:#1a1a1a;line-height:1.7}}
  h1{{color:#0F6E56;border-bottom:2px solid #E1F5EE;padding-bottom:8px}}
  h2{{color:#185FA5;margin-top:2rem}}
  strong{{color:#0F6E56}}
  hr{{border:none;border-top:1px solid #eee;margin:2rem 0}}
</style></head><body>{md_converter.markdown(report)}</body></html>"""

            st.download_button(
                label="⬇️ Download Report as HTML",
                data=html_report,
                file_name=f"{topic.lower().replace(' ', '-')}-report.html",
                mime="text/html"
            )

        except anthropic.AuthenticationError:
            st.error("❌ Invalid API key. Please check your key in the sidebar.")
        except Exception as e:
            st.error(f"❌ Something went wrong: {str(e)}")

# ── Footer ─────────────────────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; color:#aaa; font-size:0.8rem; padding: 1rem 0'>
  Built with ❤️ using Claude AI · Anthropic SDK · DuckDuckGo Search · Streamlit
</div>
""", unsafe_allow_html=True)
