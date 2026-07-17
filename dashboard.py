import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from logger import get_all_logs

st.set_page_config(
    page_title="CI/CD Failure Analyzer",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,70,245,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(56,189,248,0.08) 0%, transparent 55%),
        #080B14 !important;
    min-height: 100vh;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 40px 40px !important; max-width: 100% !important; color: #E2E8F0; }

.qm-topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 40px; height: 60px;
    background: rgba(13,17,30,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin: 0 -40px 32px;
}
.qm-logo {
    display: flex; align-items: center; gap: 10px;
    font-size: 16px; font-weight: 600; color: #F1F5F9;
}
.qm-logo-icon {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #6346F5, #38BDF8);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px;
}
.qm-status {
    display: flex; align-items: center; gap: 6px;
    font-size: 12px; font-weight: 500; color: #34D399;
    background: rgba(52,211,153,0.1);
    border: 1px solid rgba(52,211,153,0.2);
    border-radius: 20px; padding: 4px 12px;
}
.qm-dot { width: 6px; height: 6px; background: #34D399; border-radius: 50%; animation: pdot 2s infinite; }
@keyframes pdot { 0%,100%{opacity:1} 50%{opacity:0.3} }

.metric-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 16px; margin-bottom: 28px; }
.metric-card {
    background: rgba(13,17,30,0.8);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px; padding: 18px 20px;
    transition: all 0.3s;
}
.metric-card:hover { border-color: rgba(99,70,245,0.25); transform: translateY(-2px); }
.metric-label { font-size: 11px; font-weight: 500; color: #475569; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 8px; }
.metric-val { font-size: 28px; font-weight: 700; color: #F1F5F9; letter-spacing: -0.02em; line-height: 1; margin-bottom: 6px; }
.metric-sub { font-size: 11px; color: #334155; }

.card {
    background: rgba(13,17,30,0.7);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px; padding: 20px; margin-bottom: 20px;
}

.stTabs [data-baseweb="tab-list"] {
    background: rgba(13,17,30,0.5) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    padding: 4px !important; gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 8px !important;
    color: #64748B !important; font-size: 13px !important;
    font-weight: 500 !important; border: none !important; padding: 8px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,70,245,0.15) !important;
    color: #818CF8 !important; border: 1px solid rgba(99,70,245,0.25) !important;
}
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none !important; }
.stExpander {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important; border-radius: 10px !important;
}
.stExpander summary { color: #818CF8 !important; font-size: 13px !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,70,245,0.3); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# TOPBAR
st.markdown("""
<div class="qm-topbar">
    <div class="qm-logo">
        <div class="qm-logo-icon">⚡</div>
        <span>CI/CD Failure Analyzer</span>
    </div>
    <div style="font-size:13px;color:#475569;font-family:'JetBrains Mono',monospace;">
        Powered by Llama 3.3 70B · Groq · FastAPI
    </div>
    <div class="qm-status">
        <div class="qm-dot"></div>
        Listening for failures
    </div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div style="padding:8px 0 32px;">
    <div style="font-size:11px;font-weight:600;color:#6346F5;text-transform:uppercase;
    letter-spacing:0.08em;margin-bottom:12px;">⚡ AI-Powered DevOps Intelligence Platform</div>
    <div style="font-size:34px;font-weight:700;color:#F8FAFC;letter-spacing:-0.03em;
    line-height:1.1;margin-bottom:10px;">
        Pipeline failures,<br>
        <span style="background:linear-gradient(135deg,#6346F5,#38BDF8);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;">diagnosed in seconds.</span>
    </div>
    <div style="font-size:14px;color:#475569;max-width:560px;line-height:1.6;">
        Autonomous root cause analysis · LLM-powered diagnosis ·
        Automated PR comments · Real-time observability
    </div>
</div>
<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(99,70,245,0.2),transparent);margin-bottom:28px;"></div>
""", unsafe_allow_html=True)

# LOAD DATA
logs = get_all_logs()

if not logs:
    st.markdown("""
    <div style="text-align:center;padding:60px 24px;">
        <div style="font-size:48px;margin-bottom:16px;">⚡</div>
        <div style="font-size:20px;font-weight:700;color:#F1F5F9;margin-bottom:8px;">
            CI/CD Failure Analyzer is Live
        </div>
        <div style="font-size:14px;color:#475569;margin-bottom:32px;line-height:1.6;">
            The AI agent is running and listening for GitHub Actions failures.<br>
            Trigger a workflow failure to see the dashboard populate in real time.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:rgba(13,17,30,0.8);border:1px solid rgba(99,70,245,0.2);
        border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:28px;margin-bottom:8px;">🔗</div>
            <div style="font-size:13px;font-weight:600;color:#818CF8;margin-bottom:6px;">
                Step 1
            </div>
            <div style="font-size:12px;color:#475569;">
                Connect your GitHub repo via webhook pointing to the Railway server
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:rgba(13,17,30,0.8);border:1px solid rgba(99,70,245,0.2);
        border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:28px;margin-bottom:8px;">💥</div>
            <div style="font-size:13px;font-weight:600;color:#818CF8;margin-bottom:6px;">
                Step 2
            </div>
            <div style="font-size:12px;color:#475569;">
                Trigger a GitHub Actions workflow failure in your connected repo
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:rgba(13,17,30,0.8);border:1px solid rgba(99,70,245,0.2);
        border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:28px;margin-bottom:8px;">🤖</div>
            <div style="font-size:13px;font-weight:600;color:#818CF8;margin-bottom:6px;">
                Step 3
            </div>
            <div style="font-size:12px;color:#475569;">
                AI diagnoses the failure and this dashboard populates automatically
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(99,70,245,0.06);border:1px solid rgba(99,70,245,0.2);
    border-radius:12px;padding:20px 24px;max-width:600px;margin:32px auto 0;">
        <div style="font-size:13px;font-weight:600;color:#818CF8;margin-bottom:12px;">
            ⚡ AI Agent Status
        </div>
        <div style="font-size:12px;color:#64748B;line-height:2;font-family:monospace;">
            ✅ FastAPI webhook server — Railway (Live 24/7)<br>
            ✅ Llama 3.3 70B via Groq — Ready<br>
            ✅ GitHub webhook — Connected<br>
            ✅ PR comment bot — Active<br>
            ⏳ Waiting for first failure...
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    df = pd.DataFrame(logs)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["query_num"] = range(1, len(df) + 1)

    total = len(df)
    high_conf = len(df[df["confidence"] == "high"])
    pr_posted = len(df[df["pr_comment_posted"] == "Yes"])
    top_category = df["failure_category"].mode()[0] if not df.empty else "N/A"
    top_category_display = top_category.replace("_", " ").title()

    # METRIC CARDS
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div style="height:2px;margin:-18px -20px 16px;background:linear-gradient(90deg,#6346F5,#818CF8);border-radius:2px 2px 0 0;"></div>
            <div class="metric-label">Failures Analyzed</div>
            <div class="metric-val">{total}</div>
            <div class="metric-sub">Total pipeline failures</div>
        </div>
        <div class="metric-card">
            <div style="height:2px;margin:-18px -20px 16px;background:linear-gradient(90deg,#34D399,#6EE7B7);border-radius:2px 2px 0 0;"></div>
            <div class="metric-label">High Confidence</div>
            <div class="metric-val" style="color:#34D399;">{high_conf}</div>
            <div class="metric-sub">Accurate diagnoses</div>
        </div>
        <div class="metric-card">
            <div style="height:2px;margin:-18px -20px 16px;background:linear-gradient(90deg,#38BDF8,#7DD3FC);border-radius:2px 2px 0 0;"></div>
            <div class="metric-label">PR Comments Posted</div>
            <div class="metric-val" style="color:#38BDF8;">{pr_posted}</div>
            <div class="metric-sub">Developers auto-notified</div>
        </div>
        <div class="metric-card">
            <div style="height:2px;margin:-18px -20px 16px;background:linear-gradient(90deg,#FBBF24,#FDE68A);border-radius:2px 2px 0 0;"></div>
            <div class="metric-label">Top Failure Type</div>
            <div class="metric-val" style="font-size:18px;color:#FBBF24;">{top_category_display}</div>
            <div class="metric-sub">Most recurring pattern</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📊  Analytics Dashboard",
        "🔍  Failure Details",
        "🗂️  Full Log"
    ])

    # TAB 1 - ANALYTICS
    with tab1:
        col1, col2 = st.columns(2, gap="large")

        with col1:
            cat_counts = df["failure_category"].value_counts().reset_index()
            cat_counts.columns = ["category", "count"]
            cat_counts["category"] = cat_counts["category"].str.replace("_", " ").str.title()

            fig_cat = go.Figure(go.Bar(
                x=cat_counts["count"], y=cat_counts["category"],
                orientation="h",
                marker=dict(color="#6346F5", line=dict(color="rgba(99,70,245,0.3)", width=1)),
                hovertemplate="<b>%{y}</b><br>%{x} failures<extra></extra>"
            ))
            fig_cat.update_layout(
                title=dict(text="Failures by Category", font=dict(color="#F1F5F9", size=14, family="Inter")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#64748B", size=11),
                xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False, tickfont=dict(color="#334155")),
                yaxis=dict(showgrid=False, tickfont=dict(color="#94A3B8")),
                margin=dict(l=0, r=0, t=40, b=0), height=300
            )
            st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

        with col2:
            conf_counts = df["confidence"].value_counts()
            fig_conf = go.Figure(go.Pie(
                labels=conf_counts.index.tolist(),
                values=conf_counts.values.tolist(),
                hole=0.62,
                marker=dict(colors=["#34D399", "#FBBF24", "#F87171"], line=dict(color="rgba(0,0,0,0)", width=0)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value} diagnoses<extra></extra>"
            ))
            fig_conf.add_annotation(
                text=str(total), x=0.5, y=0.55,
                font=dict(size=26, color="#F1F5F9", family="Inter"), showarrow=False
            )
            fig_conf.add_annotation(
                text="total", x=0.5, y=0.38,
                font=dict(size=11, color="#475569", family="Inter"), showarrow=False
            )
            fig_conf.update_layout(
                title=dict(text="Diagnosis Confidence", font=dict(color="#F1F5F9", size=14, family="Inter")),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#64748B", size=11), orientation="h", x=0.1, y=-0.1),
                margin=dict(l=0, r=0, t=40, b=40), height=300
            )
            st.plotly_chart(fig_conf, use_container_width=True, config={"displayModeBar": False})

        fig_time = px.scatter(
            df, x="timestamp", y="failure_category",
            color="confidence", size_max=14,
            title="Failure Timeline",
            color_discrete_map={"high": "#34D399", "medium": "#FBBF24", "low": "#F87171"},
            hover_data=["repo", "workflow", "branch"]
        )
        fig_time.update_traces(marker=dict(size=12, opacity=0.85))
        fig_time.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#64748B", size=11),
            title_font=dict(color="#F1F5F9", size=14),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False, tickfont=dict(color="#334155")),
            yaxis=dict(showgrid=False, tickfont=dict(color="#94A3B8"), title=None),
            legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#64748B", size=11)),
            margin=dict(l=0, r=0, t=40, b=0), height=260
        )
        st.plotly_chart(fig_time, use_container_width=True, config={"displayModeBar": False})

        col3, col4 = st.columns(2, gap="large")
        with col3:
            branch_counts = df["branch"].value_counts().head(8).reset_index()
            branch_counts.columns = ["branch", "count"]
            fig_branch = px.bar(branch_counts, x="branch", y="count",
                title="Failures by Branch", color_discrete_sequence=["#38BDF8"])
            fig_branch.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#64748B", size=11),
                title_font=dict(color="#F1F5F9", size=14),
                xaxis=dict(showgrid=False, tickfont=dict(color="#94A3B8")),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#334155")),
                margin=dict(l=0, r=0, t=40, b=0), height=240
            )
            st.plotly_chart(fig_branch, use_container_width=True, config={"displayModeBar": False})

        with col4:
            pr_data = df["pr_comment_posted"].value_counts().reset_index()
            pr_data.columns = ["status", "count"]
            fig_pr = go.Figure(go.Bar(
                x=pr_data["status"], y=pr_data["count"],
                marker=dict(
                    color=["#34D399" if s == "Yes" else "#F87171" for s in pr_data["status"]],
                    line=dict(color="rgba(0,0,0,0)", width=0)
                ),
                hovertemplate="<b>%{x}</b><br>%{y} failures<extra></extra>"
            ))
            fig_pr.update_layout(
                title=dict(text="PR Comment Status", font=dict(color="#F1F5F9", size=14, family="Inter")),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#64748B", size=11),
                xaxis=dict(showgrid=False, tickfont=dict(color="#94A3B8")),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", tickfont=dict(color="#334155")),
                margin=dict(l=0, r=0, t=40, b=0), height=240
            )
            st.plotly_chart(fig_pr, use_container_width=True, config={"displayModeBar": False})

    # TAB 2 - FAILURE DETAILS
    with tab2:
        category_emoji = {
            "missing_dependency": "📦", "failing_test": "🧪",
            "syntax_error": "🔴", "environment_variable": "🔑",
            "flaky_test": "⚠️", "docker_error": "🐳",
            "permission_error": "🔒", "timeout": "⏱️",
            "infrastructure": "🏗️", "other": "🔍"
        }
        confidence_color = {"high": "#34D399", "medium": "#FBBF24", "low": "#F87171"}

        for _, row in df.iterrows():
            emoji = category_emoji.get(row["failure_category"], "🔍")
            cat_display = row["failure_category"].replace("_", " ").title()
            conf_color = confidence_color.get(row["confidence"], "#FBBF24")
            ts = row["timestamp"]
            ts_str = ts.strftime("%b %d, %H:%M") if hasattr(ts, "strftime") else str(ts)[:16]
            sha = row["commit_sha"] if row["commit_sha"] else "unknown"

            with st.expander(f"{emoji}  {row['repo']} — {row['workflow']} — {cat_display} — {ts_str}"):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Repository</div>
                        <div style="font-size:13px;color:#CBD5E1;font-family:monospace;">{row['repo']}</div>
                    </div>
                    <div style="margin-bottom:12px;">
                        <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Workflow</div>
                        <div style="font-size:13px;color:#CBD5E1;">{row['workflow']}</div>
                    </div>
                    <div>
                        <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Branch · Commit</div>
                        <div style="font-size:13px;color:#CBD5E1;font-family:monospace;">{row['branch']} · {sha}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div style="margin-bottom:12px;">
                        <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Failure Category</div>
                        <div style="font-size:13px;color:#818CF8;">{cat_display}</div>
                    </div>
                    <div style="margin-bottom:12px;">
                        <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Confidence</div>
                        <div style="font-size:13px;font-weight:600;color:{conf_color};">{row['confidence'].upper()}</div>
                    </div>
                    <div>
                        <div style="font-size:11px;color:#475569;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">PR Comment</div>
                        <div style="font-size:13px;color:#CBD5E1;">{row['pr_comment_posted']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                root_cause = row['root_cause'] if row['root_cause'] else 'No root cause available'
                suggested_fix = row['suggested_fix'] if row['suggested_fix'] else 'No fix available'

                st.markdown(f"""
                <div style="background:rgba(99,70,245,0.05);border:1px solid rgba(99,70,245,0.15);
                border-left:3px solid #6346F5;border-radius:0 10px 10px 0;padding:14px 16px;margin-top:12px;margin-bottom:10px;">
                    <div style="font-size:11px;font-weight:600;color:#6346F5;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">🔍 Root Cause</div>
                    <div style="font-size:13px;color:#CBD5E1;line-height:1.7;">{root_cause}</div>
                </div>
                <div style="background:rgba(52,211,153,0.05);border:1px solid rgba(52,211,153,0.15);
                border-left:3px solid #34D399;border-radius:0 10px 10px 0;padding:14px 16px;">
                    <div style="font-size:11px;font-weight:600;color:#34D399;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">🛠️ Suggested Fix</div>
                    <div style="font-size:13px;color:#CBD5E1;line-height:1.7;">{suggested_fix}</div>
                </div>
                """, unsafe_allow_html=True)

    # TAB 3 - FULL LOG
    with tab3:
        st.markdown("""
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="font-size:14px;font-weight:600;color:#F1F5F9;">🗂️ Complete Failure Log</div>
            <div style="font-size:11px;color:#818CF8;background:rgba(99,70,245,0.12);
            border:1px solid rgba(99,70,245,0.2);border-radius:4px;padding:3px 9px;">Auto-updated</div>
        </div>
        """, unsafe_allow_html=True)

        display_df = df[["repo", "workflow", "branch", "commit_sha",
                         "failure_category", "confidence", "pr_comment_posted", "timestamp"]].copy()
        display_df.columns = ["Repository", "Workflow", "Branch", "Commit",
                               "Failure Category", "Confidence", "PR Comment", "Timestamp"]
        display_df["Failure Category"] = display_df["Failure Category"].str.replace("_", " ").str.title()
        display_df["Timestamp"] = pd.to_datetime(display_df["Timestamp"]).dt.strftime("%b %d, %H:%M")

        st.dataframe(
            display_df, use_container_width=True, hide_index=True,
            column_config={
                "Repository": st.column_config.TextColumn(width="medium"),
                "Workflow": st.column_config.TextColumn(width="medium"),
                "Branch": st.column_config.TextColumn(width="small"),
                "Commit": st.column_config.TextColumn(width="small"),
                "Failure Category": st.column_config.TextColumn(width="medium"),
                "Confidence": st.column_config.TextColumn(width="small"),
                "PR Comment": st.column_config.TextColumn(width="small"),
                "Timestamp": st.column_config.TextColumn(width="small"),
            }
        )

# FOOTER
st.markdown("""
<div style="text-align:center;padding:32px 0;border-top:1px solid rgba(255,255,255,0.04);margin-top:32px;">
    <div style="font-size:11px;color:#1E293B;font-family:'JetBrains Mono',monospace;">
        CI/CD Failure Analyzer · LangChain · Groq · Llama 3.3 70B · FastAPI · Streamlit
    </div>
</div>
""", unsafe_allow_html=True)