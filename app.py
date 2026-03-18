import streamlit as st
import anthropic
from duckduckgo_search import DDGS
import markdown as md_converter
import time

st.set_page_config(
    page_title="Periscope · AI Research Agent",
    page_icon="🔭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp { font-family: 'DM Sans', sans-serif; background-color: #0A0A0F !important; color: #E8E6E0; }
.stApp { background: #0A0A0F !important; }

.nav { display: flex; align-items: center; justify-content: space-between; padding: 1.5rem 0 2.5rem; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 4rem; }
.nav-logo { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 800; letter-spacing: -0.02em; color: #F0EDE6; }
.nav-logo span { color: #C8F04D; }
.nav-tag { font-size: 0.7rem; font-weight: 500; letter-spacing: 0.12em; text-transform: uppercase; color: rgba(255,255,255,0.3); border: 1px solid rgba(255,255,255,0.1); padding: 4px 10px; border-radius: 20px; }

.hero-eyebrow { font-size: 0.72rem; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #C8F04D; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 8px; }
.hero-eyebrow::before { content: ''; display: inline-block; width: 20px; height: 1px; background: #C8F04D; }
.hero-title { font-family: 'Syne', sans-serif; font-size: clamp(2.4rem, 5vw, 3.8rem); font-weight: 800; line-height: 1.05; letter-spacing: -0.03em; color: #F0EDE6; margin-bottom: 1.25rem; }
.hero-title em { font-style: normal; color: transparent; -webkit-text-stroke: 1px rgba(240,237,230,0.4); }
.hero-sub { font-size: 1rem; font-weight: 300; line-height: 1.7; color: rgba(232,230,224,0.55); max-width: 480px; margin-bottom: 2.5rem; }

.pill-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 3.5rem; }
.pill { display: inline-flex; align-items: center; gap: 6px; font-size: 0.78rem; font-weight: 400; color: rgba(232,230,224,0.6); background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 6px 14px; }
.pill-dot { width: 5px; height: 5px; border-radius: 50%; background: #C8F04D; flex-shrink: 0; }

.form-label { font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(232,230,224,0.4); margin-bottom: 0.6rem; }
.stTextInput > div > div > input { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.1) !important; border-radius: 12px !important; color: #F0EDE6 !important; font-family: 'DM Sans', sans-serif !important; font-size: 1rem !important; font-weight: 300 !important; padding: 14px 18px !important; transition: border-color 0.2s !important; }
.stTextInput > div > div > input:focus { border-color: #C8F04D !important; box-shadow: 0 0 0 3px rgba(200,240,77,0.08) !important; }
.stTextInput > div > div > input::placeholder { color: rgba(232,230,224,0.25) !important; }

.ex-label { font-size: 0.72rem; letter-spacing: 0.1em; text-transform: uppercase; color: rgba(232,230,224,0.3); margin: 1rem 0 0.6rem; }
.stButton > button { background: rgba(255,255,255,0.04) !important; color: rgba(232,230,224,0.65) !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 400 !important; padding: 6px 14px !important; transition: all 0.15s !important; width: 100% !important; }
.stButton > button:hover { background: rgba(200,240,77,0.08) !important; border-color: rgba(200,240,77,0.3) !important; color: #C8F04D !important; }

.search-log { background: #111118; border: 1px solid rgba(200,240,77,0.15); border-left: 3px solid #C8F04D; border-radius: 10px; padding: 1rem 1.25rem; font-family: 'Courier New', monospace; font-size: 0.82rem; color: rgba(200,240,77,0.8); line-height: 1.8; margin: 1rem 0; }

.stProgress > div > div { background: rgba(255,255,255,0.06) !important; border-radius: 4px !important; }
.stProgress > div > div > div { background: #C8F04D !important; border-radius: 4px !important; }

.metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 1.5rem 0; }
.metric-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 12px; padding: 1rem; text-align: center; }
.metric-card .num { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; color: #C8F04D; line-height: 1; margin-bottom: 4px; }
.metric-card .lbl { font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: rgba(232,230,224,0.35); }

.report-wrap { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 2.5rem; margin-top: 1.5rem; }
.report-wrap h1 { font-family: 'Syne', sans-serif !important; font-size: 1.6rem !important; font-weight: 800 !important; color: #F0EDE6 !important; border-bottom: 1px solid rgba(255,255,255,0.08) !important; padding-bottom: 0.75rem !important; margin-bottom: 1.5rem !important; }
.report-wrap h2 { font-family: 'Syne', sans-serif !important; font-size: 1.15rem !important; font-weight: 700 !important; color: #C8F04D !important; margin-top: 2rem !important; margin-bottom: 0.75rem !important; }
.report-wrap h3 { font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; color: rgba(232,230,224,0.5) !important; margin-top: 1.25rem !important; margin-bottom: 0.4rem !important; }
.report-wrap p, .report-wrap li { font-size: 0.95rem !important; line-height: 1.8 !important; color: rgba(232,230,224,0.75) !important; }
.report-wrap strong { color: #F0EDE6 !important; font-weight: 500 !important; }
.report-wrap hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }
.report-wrap ul { padding-left: 1.25rem !important; }
.report-wrap li { margin: 6px 0 !important; }

.section-header { display: flex; align-items: center; gap: 10px; margin-bottom: 0.75rem; }
.section-num { font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700; color: #C8F04D; background: rgba(200,240,77,0.1); border: 1px solid rgba(200,240,77,0.2); border-radius: 6px; padding: 2px 8px; }
.section-title { font-family: 'Syne', sans-serif; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.14em; text-transform: uppercase; color: rgba(232,230,224,0.4); }

.stDownloadButton > button { background: transparent !important; color: rgba(232,230,224,0.6) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.85rem !important; padding: 10px 20px !important; width: auto !important; }
.stDownloadButton > button:hover { border-color: rgba(200,240,77,0.4) !important; color: #C8F04D !important; }

.run-btn > div > .stButton > button { background: #C8F04D !important; color: #0A0A0F !important; border: none !important; border-radius: 12px !important; font-family: 'Syne', sans-serif !important; font-size: 0.95rem !important; font-weight: 700 !important; padding: 14px 32px !important; width: 100% !important; }
.run-btn > div > .stButton > button:hover { background: #d8ff5a !important; }

.footer { text-align: center; padding: 3rem 0 2rem; font-size: 0.78rem; color: rgba(232,230,224,0.2); letter-spacing: 0.04em; }
.footer span { color: rgba(200,240,77,0.5); }

footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
.stDeployButton { display: none; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav">
  <div class="nav-logo">Periscope<span>.</span></div>
  <div class="nav-tag">AI Research Agent</div>
</div>
<div class="hero-eyebrow">Competitive Intelligence</div>
<div class="hero-title">Research any market.<br><em>Instantly.</em></div>
<div class="hero-sub">Enter a topic and watch the agent autonomously search the web, analyse competitors, and deliver a structured intelligence report — in under a minute.</div>
<div class="pill-row">
  <div class="pill"><div class="pill-dot"></div>Live web search</div>
  <div class="pill"><div class="pill-dot"></div>Claude AI synthesis</div>
  <div class="pill"><div class="pill-dot"></div>Positioning · Differentiation · Impact</div>
  <div class="pill"><div class="pill-dot"></div>Downloadable report</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="form-label">01 — Research topic</div>', unsafe_allow_html=True)
topic = st.text_input("", placeholder="e.g. AI coding assistants, CRM software, no-code builders...", label_visibility="collapsed", key="topic_input")

st.markdown('<div class="ex-label">Quick start</div>', unsafe_allow_html=True)
ex_cols = st.columns(4)
examples = ["AI writing tools", "No-code builders", "CRM software", "Product analytics"]
for i, ex in enumerate(examples):
    with ex_cols[i]:
        if st.button(ex, key=f"ex_{i}"):
            topic = ex

st.markdown('<div class="form-label" style="margin-top:1.5rem;">02 — Anthropic API key</div>', unsafe_allow_html=True)
api_key = st.text_input("", type="password", placeholder="sk-ant-api03-...", label_visibility="collapsed", key="api_key_input")
st.markdown('<div style="font-size:0.75rem; color:rgba(232,230,224,0.25); margin-top:6px;">Your key is never stored. Get one at <a href="https://console.anthropic.com" style="color:rgba(200,240,77,0.5);">console.anthropic.com</a></div>', unsafe_allow_html=True)

st.markdown('<div class="run-btn" style="margin-top:2rem;">', unsafe_allow_html=True)
run_clicked = st.button("Run research agent →", key="run_btn")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("How does this agent work?"):
    st.markdown("""
    **This is an AI Agent — not a chatbot.** Here's what happens when you hit Run:
    1. **Claude AI** receives your topic and decides what to search for
    2. It autonomously calls **DuckDuckGo** multiple times with different queries
    3. It reads and cross-references all search results
    4. It synthesises a structured report: **Positioning · Differentiation · Impact · Market Sentiment**
    5. You get a downloadable report and a live preview

    Built by **Chirag Mewara** using the Anthropic SDK, DuckDuckGo Search, and Streamlit.
    """)

def search_web(query):
    try:
        results = DDGS().text(query, max_results=5)
        if not results:
            return "No results found."
        return "\n---\n".join([f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}" for r in results])
    except Exception as e:
        return f"Search failed: {str(e)}"

def run_agent(topic, api_key, log_container, progress_bar):
    client = anthropic.Anthropic(api_key=api_key)
    tools = [{"name": "web_search", "description": "Search the web for current information.", "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}]
    system_prompt = """You are a deep research agent that creates competitor analysis reports.
When given a topic, you MUST:
1. Search the web at least 3 times with different queries
2. Write a structured Markdown report covering the top 3 competitors with:
   - **Positioning**, **Differentiation**, **Impact**, **Market Sentiment**
3. End with '## Key Takeaways' with 3-4 bullet points
Be specific and data-driven."""
    messages = [{"role": "user", "content": f"Research competitive landscape for: {topic}. Write a detailed competitor analysis report."}]
    searches_done = 0
    log_lines = []
    progress_bar.progress(10)
    while True:
        response = client.messages.create(model="claude-sonnet-4-20250514", max_tokens=4096, system=system_prompt, tools=tools, messages=messages)
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
                    log_lines.append(f"→ [{searches_done}] {query}")
                    log_container.markdown(f'<div class="search-log">' + '<br>'.join(log_lines) + '</div>', unsafe_allow_html=True)
                    progress_bar.progress(min(10 + searches_done * 20, 85))
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": search_web(query)})
            messages.append({"role": "user", "content": tool_results})

if run_clicked:
    if not topic:
        st.warning("Please enter a research topic above.")
    elif not api_key:
        st.warning("Please enter your Anthropic API key above.")
    else:
        st.divider()
        st.markdown('<div class="section-header"><div class="section-num">LIVE</div><div class="section-title">Agent running</div></div>', unsafe_allow_html=True)
        progress = st.progress(0)
        log_box = st.empty()
        status = st.empty()
        try:
            start = time.time()
            report, num_searches = run_agent(topic, api_key, log_box, progress)
            elapsed = round(time.time() - start, 1)
            status.success(f"Research complete — {num_searches} searches · {elapsed}s")
            word_count = len(report.split())
            st.markdown(f'<div class="metrics-row"><div class="metric-card"><div class="num">{num_searches}</div><div class="lbl">Searches run</div></div><div class="metric-card"><div class="num">{word_count}</div><div class="lbl">Words written</div></div><div class="metric-card"><div class="num">{elapsed}s</div><div class="lbl">Time taken</div></div></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-header" style="margin-top:2rem;"><div class="section-num">REPORT</div><div class="section-title">Competitor analysis</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="report-wrap">', unsafe_allow_html=True)
            st.markdown(report)
            st.markdown('</div>', unsafe_allow_html=True)
            html_report = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{topic} — Periscope</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:'DM Sans',sans-serif;background:#0A0A0F;color:#E8E6E0;max-width:760px;margin:0 auto;padding:3rem 2rem;line-height:1.8}}h1{{font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:#F0EDE6;border-bottom:1px solid rgba(255,255,255,0.08);padding-bottom:1rem;margin-bottom:2rem}}h2{{font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#C8F04D;margin-top:2.5rem;margin-bottom:0.75rem}}h3{{font-size:0.78rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:rgba(232,230,224,0.4);margin-top:1.5rem;margin-bottom:0.5rem}}p,li{{font-size:0.95rem;color:rgba(232,230,224,0.7);line-height:1.8}}strong{{color:#F0EDE6;font-weight:500}}ul{{padding-left:1.25rem}}li{{margin:6px 0}}hr{{border:none;border-top:1px solid rgba(255,255,255,0.06);margin:2rem 0}}.meta{{font-size:0.75rem;color:rgba(232,230,224,0.2);text-align:right;margin-top:3rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.06)}}</style>
</head><body>{md_converter.markdown(report)}<div class="meta">Generated by Periscope · Built by Chirag Mewara</div></body></html>"""
            st.download_button(label="↓ Download report", data=html_report, file_name=f"{topic.lower().replace(' ', '-')}-report.html", mime="text/html")
        except anthropic.AuthenticationError:
            st.error("Invalid API key — please check and try again.")
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown('<div class="footer">Periscope · Built by <span>Chirag Mewara</span> · Powered by Claude AI & DuckDuckGo</div>', unsafe_allow_html=True)
