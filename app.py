import time
import datetime
import streamlit as st
from pipeline import run_research_pipeline


st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,500;0,6..72,600;0,6..72,700;1,6..72,500&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #E8E6E1; }

.stApp {
    background-color: #0F1115;
    background-image:
        radial-gradient(ellipse 60% 45% at 12% -8%, rgba(110,123,255,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 55% 40% at 90% 105%, rgba(45,212,191,0.07) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.6rem 3rem 4rem; max-width: 1240px; }

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}

/* ── Masthead ── */
.masthead { border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 1.2rem; margin-bottom: 1.9rem; }
.masthead-eyebrow {
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: #F5B342; margin-bottom: 0.7rem;
}
.masthead-title {
    font-family: 'Newsreader', serif; font-weight: 700; font-size: clamp(2rem, 4vw, 3.1rem);
    letter-spacing: -0.01em; line-height: 1.08; margin: 0 0 0.6rem; color: #F3F1EC;
}
.masthead-sub { font-size: 1rem; color: #8B8D98; max-width: 640px; line-height: 1.6; font-weight: 400; }

/* ── Query console ── */
.query-panel {
    background: #171A21; border: 1px solid rgba(255,255,255,0.09); border-radius: 10px;
    padding: 1.7rem 2rem; margin-bottom: 1.1rem; box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.query-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: #6E7BFF; margin-bottom: 0.6rem; display: block;
}
.stTextInput > div > div > input {
    background: #0F1115 !important; border: 1.5px solid rgba(255,255,255,0.14) !important;
    border-radius: 6px !important; color: #E8E6E1 !important; font-family: 'Inter', sans-serif !important;
    font-size: 1.02rem !important; padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input::placeholder { color: #5C5F6B !important; }
.stTextInput > div > div > input:focus {
    border-color: #6E7BFF !important; box-shadow: 0 0 0 3px rgba(110,123,255,0.2) !important;
}
.stTextInput > label { display: none !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6E7BFF 0%, #5563E8 100%) !important; color: #0F1115 !important;
    font-family: 'Inter', sans-serif !important; font-weight: 700 !important; font-size: 0.92rem !important;
    letter-spacing: 0.01em !important; border: none !important; border-radius: 8px !important;
    padding: 0.68rem 1.4rem !important; box-shadow: 0 4px 18px rgba(110,123,255,0.3) !important;
    transition: transform 0.12s, box-shadow 0.12s !important; width: 100%;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 22px rgba(110,123,255,0.4) !important; }
.stButton > button:active { transform: translateY(0) !important; }

.chip-caption {
    font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #6b6e78; letter-spacing: 0.14em;
    text-transform: uppercase; margin: 0.9rem 0 0.5rem;
}

/* ── Agent line (contributors) ── */
.agents-heading {
    font-family: 'Newsreader', serif; font-weight: 700; font-size: 1.2rem; margin: 0 0 1rem; color: #F3F1EC;
}
.agent-card {
    background: #171A21; border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid rgba(255,255,255,0.12);
    border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.7rem; position: relative;
    transition: border-color 0.3s, background 0.3s;
}
.agent-card.done { border-left-color: #F5B342; background: #1D1B14; }
.agent-top { display: flex; align-items: center; gap: 0.6rem; }
.agent-num { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; color: #6E7BFF; opacity: 0.9; }
.agent-name { font-family: 'Inter', sans-serif; font-weight: 600; font-size: 0.88rem; color: #E8E6E1; }
.agent-badge {
    margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; letter-spacing: 0.08em;
    padding: 0.15rem 0.5rem; border-radius: 4px;
}
.badge-pending { color: #6b6e78; background: rgba(255,255,255,0.05); }
.badge-done { color: #F5B342; background: rgba(245,179,66,0.14); font-weight: 600; }
.agent-desc { font-size: 0.76rem; color: #8B8D98; margin: 0.2rem 0 0 1.55rem; }

/* ── Divider ── */
.rule { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 2.2rem 0 1.6rem; }

/* ── Stats row ── */
.stats-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 1.3rem; }
.stat-pill {
    background: #171A21; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px;
    padding: 0.4rem 0.95rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #8B8D98;
}
.stat-pill b { color: #E8E6E1; }

/* ── Research brief (report) ── */
.brief {
    background: #171A21; border: 1px solid rgba(110,123,255,0.22); border-radius: 12px;
    padding: 2.4rem 2.8rem; margin-top: 0.3rem; box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.brief-kicker {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: #F5B342; margin-bottom: 0.5rem;
}
.brief-title {
    font-family: 'Newsreader', serif; font-style: italic; font-weight: 600; font-size: 1.7rem;
    margin: 0 0 0.5rem; color: #F3F1EC;
}
.brief-byline { font-family: 'Inter', sans-serif; font-size: 0.8rem; color: #8B8D98; margin-bottom: 1.4rem; }
.brief-body {
    font-family: 'Newsreader', serif; font-size: 1.06rem; line-height: 1.75; color: #DAD7CF;
    max-width: 720px;
}
.brief-body h1, .brief-body h2, .brief-body h3 { font-family: 'Newsreader', serif; font-weight: 700; color: #F3F1EC; }
.brief-body a { color: #8FA0FF; }

/* ── Peer review (critic) ── */
.review {
    background: #12211D; border: 1px solid rgba(45,212,191,0.28); border-radius: 12px;
    padding: 1.8rem 2.2rem; margin-top: 1.4rem;
}
.review-kicker {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase;
    color: #2DD4BF; margin-bottom: 0.9rem;
}
.review-body { font-family: 'Inter', sans-serif; font-size: 0.94rem; line-height: 1.7; color: #C9E8E2; }
.review-sig { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #2DD4BF; margin-top: 1rem; }

.footer-note {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #5C5F6B; text-align: center;
    margin-top: 3rem; letter-spacing: 0.08em;
}

/* ── Streamlit misc dark tweaks ── */
[data-testid="stSidebar"] { background-color: #0D0F13; border-right: 1px solid rgba(255,255,255,0.07); }
[data-testid="stExpander"] { background-color: #171A21; border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; }
.stAlert { background-color: #171A21 !important; }
</style>
""", unsafe_allow_html=True)


if "result" not in st.session_state:
    st.session_state.result = None
if "topic" not in st.session_state:
    st.session_state.topic = ""
if "elapsed" not in st.session_state:
    st.session_state.elapsed = None
if "issue_no" not in st.session_state:
    st.session_state.issue_no = None
if "pending_topic" not in st.session_state:
    st.session_state.pending_topic = None

EXAMPLE_TOPICS = ["LLM agents in 2026", "CRISPR gene editing", "Fusion energy progress"]


with st.sidebar:
    st.markdown("### 📰 Research System")
    st.caption("A four-agent research pipeline")
    st.divider()
    st.markdown(
        """
        **How it works**

        `01` 🔎 **Search Agent** — finds recent, reliable sources
        `02` 📖 **Reader Agent** — reads the top source in depth
        `03` ✍️ **Writer Agent** — drafts the research brief
        `04` 🧭 **Critic Agent** — reviews the draft for gaps
        """
    )
    st.divider()
    if st.session_state.result:
        st.markdown(f"**Issue No.** `{st.session_state.issue_no}`")
        st.caption(f"Completed in {st.session_state.elapsed:.1f}s")
    st.caption("Built with LangChain + Streamlit")


st.markdown(f"""
<div class="masthead">
    <div class="masthead-eyebrow">Multi-Agent Research System</div>
    <h1 class="masthead-title">Turn any topic into a reviewed research brief.</h1>
    <div class="masthead-sub">
        Four agents work in sequence — searching, reading, writing, and reviewing —
        so you get a finished, fact-checked brief instead of a pile of tabs.
    </div>
</div>
""", unsafe_allow_html=True)


col_input, col_gap, col_agents = st.columns([5, 0.4, 4])

with col_input:
    st.markdown('<div class="query-panel">', unsafe_allow_html=True)
    st.markdown('<span class="query-label">Research Topic</span>', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        value=st.session_state.topic,
        placeholder="e.g. Latest advances in solid-state batteries",
        key="topic_input",
        label_visibility="collapsed",
    )
    run_clicked = st.button("Run Research →", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chip-caption">Or try a topic →</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(EXAMPLE_TOPICS))
    for c, ex in zip(chip_cols, EXAMPLE_TOPICS):
        if c.button(ex, key=f"chip_{ex}", use_container_width=True):
            st.session_state.pending_topic = ex
            st.rerun()

    if st.session_state.result:
        st.button(
            "Clear this brief",
            on_click=lambda: st.session_state.update(result=None, topic="", elapsed=None, issue_no=None),
        )

with col_agents:
    st.markdown('<div class="agents-heading">Agents on this run</div>', unsafe_allow_html=True)
    r = st.session_state.result

    def agent_card(num, name, desc, key):
        is_done = bool(r and key in r)
        card_cls = "done" if is_done else ""
        badge_label = "COMPLETE" if is_done else "WAITING"
        badge_cls = "badge-done" if is_done else "badge-pending"
        st.markdown(f"""
        <div class="agent-card {card_cls}">
            <div class="agent-top">
                <span class="agent-num">{num}</span>
                <span class="agent-name">{name}</span>
                <span class="agent-badge {badge_cls}">{badge_label}</span>
            </div>
            <div class="agent-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    agent_card("01", "Search Agent", "Finds recent, reliable sources", "search_results")
    agent_card("02", "Reader Agent", "Reads the top source in depth", "scraped_content")
    agent_card("03", "Writer Agent", "Drafts the research brief", "report")
    agent_card("04", "Critic Agent", "Reviews the draft for gaps", "feedback")


if st.session_state.pending_topic:
    topic = st.session_state.pending_topic
    st.session_state.pending_topic = None
    run_clicked = True


if run_clicked:
    if not topic.strip():
        st.warning("Enter a research topic before running the pipeline.")
    else:
        st.session_state.topic = topic
        with st.status("Running the research pipeline…", expanded=True) as status:
            start = time.time()
            try:
                status.update(label="🔎 Search Agent is finding sources…")
                result = run_research_pipeline(topic)
                st.session_state.result = result
                st.session_state.elapsed = time.time() - start
                st.session_state.issue_no = datetime.datetime.now().strftime("%Y.%m%d-%H%M")
                status.update(label="✅ Research brief ready", state="complete", expanded=False)
                        except Exception as e:
                status.update(
                    label=f"❌ Pipeline failed: {e}",
                    state="error",
                    expanded=True,
                )
                st.session_state.result = None


r = st.session_state.result

if r:
    st.markdown('<hr class="rule">', unsafe_allow_html=True)

    report_text = str(r.get("report", ""))
    feedback_text = str(r.get("feedback", ""))
    word_count = len(report_text.split())

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-pill">TOPIC: <b>{st.session_state.topic}</b></div>
        <div class="stat-pill">LENGTH: <b>{word_count} words</b></div>
        <div class="stat-pill">RUNTIME: <b>{st.session_state.elapsed:.1f}s</b></div>
        <div class="stat-pill">ISSUE: <b>{st.session_state.issue_no}</b></div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🔎 Raw search results"):
        st.text(r.get("search_results", ""))
    with st.expander("📖 Raw scraped content"):
        st.text(r.get("scraped_content", ""))

    st.markdown(f"""
    <div class="brief">
        <div class="brief-kicker">Research Brief</div>
        <div class="brief-title">{st.session_state.topic}</div>
        <div class="brief-byline">Drafted by the Writer Agent · Reviewed by the Critic Agent</div>
        <div class="brief-body">
    """, unsafe_allow_html=True)
    st.markdown(report_text)
    st.markdown('</div></div>', unsafe_allow_html=True)

    st.download_button(
        "⬇  Download brief (.md)",
        data=report_text,
        file_name=f"{st.session_state.topic.replace(' ', '_')}_brief.md",
        mime="text/markdown",
    )

    st.markdown('<div class="review"><div class="review-kicker">Peer Review — Critic Agent</div><div class="review-body">', unsafe_allow_html=True)
    st.markdown(feedback_text)
    st.markdown('<div class="review-sig">— Critic Agent</div></div></div>', unsafe_allow_html=True)
else:
    st.info("Enter a topic above (or try an example) and click **Run Research →** to get started.")


st.markdown("""
<div class="footer-note">MULTI-AGENT RESEARCH SYSTEM · LANGCHAIN PIPELINE · BUILT WITH STREAMLIT</div>
""", unsafe_allow_html=True)
