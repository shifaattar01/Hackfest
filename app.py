
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="EstiMateAi | Estimate Smarter, Build Better",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM THEME ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 10% 0%,
        #201044 0, #0a0b18 38%, #05060b 100%);
    color: #f5f6ff;
}

.block-container {
    padding-top: 1.6rem;
    max-width: 1320px;
}

[data-testid="stSidebar"] {
    background: #0c0d1b;
    border-right: 1px solid #27213e;
}

h1, h2, h3 {
    color: #f8f7ff;
}

p, label, .stMarkdown {
    color: #d7d8e8;
}

.brand {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: white;
}

.brand span {
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.tagline {
    font-size: 1.1rem;
    color: #c4c5d8;
}

.metric-card {
    background: linear-gradient(
        145deg,
        rgba(124,58,237,.18),
        rgba(37,99,235,.09)
    );
    border: 1px solid rgba(167,139,250,.3);
    border-radius: 16px;
    padding: 18px;
    min-height: 120px;
}

.metric-label {
    font-size: .82rem;
    color: #b9bad0;
    margin-bottom: 9px;
}

.metric-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: white;
}

.metric-sub {
    font-size: .78rem;
    color: #a78bfa;
    margin-top: 6px;
}

div.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #2563eb);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    padding: .65rem 1.1rem;
}

div.stButton > button:hover {
    border: 1px solid #a78bfa;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------------- HELPER FUNCTIONS ----------------

def money(value):
    return "₹{:,.0f}".format(max(0, value))


def estimate_project(
    team_size,
    experience,
    complexity,
    features,
    months,
    dev_rate,
    tester_rate,
    manager_rate,
    cloud_monthly,
    tools_monthly,
    contingency_pct
):
    # Demonstration formula.
    # This is not a trained machine-learning model.

    complexity_factor = {
        "Low": 0.8,
        "Medium": 1.0,
        "High": 1.35,
        "Very high": 1.7
    }[complexity]

    experience_factor = max(
        0.72, 1.12 - experience * 0.045
    )

    feature_factor = max(0.5, features / 20)

    total_hours = (
        team_size
        * months
        * 140
        * complexity_factor
        * experience_factor
        * feature_factor
    )

    dev_hours = total_hours * 0.62
    test_hours = total_hours * 0.25
    manager_hours = total_hours * 0.13

    personnel_cost = (
        dev_hours * dev_rate
        + test_hours * tester_rate
        + manager_hours * manager_rate
    )

    cloud_cost = cloud_monthly * months
    tool_cost = tools_monthly * months

    subtotal = personnel_cost + cloud_cost + tool_cost
    contingency = subtotal * contingency_pct / 100
    total_cost = subtotal + contingency

    return {
        "development_hours": dev_hours,
        "testing_hours": test_hours,
        "management_hours": manager_hours,
        "total_effort": total_hours,
        "personnel_cost": personnel_cost,
        "cloud_cost": cloud_cost,
        "tool_cost": tool_cost,
        "contingency": contingency,
        "total_cost": total_cost,
        "duration_months": months
    }


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown("## 🟣 EstiMateAi")
    st.caption("Estimate Smarter, Build Better")

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Cost Estimator",
            "Scenario Planner",
            "Dataset Explorer",
            "About"
        ]
    )

    st.divider()
    st.caption("Prototype v1.0")
    st.caption("Purple • Blue • Black")


# ---------------- BRAND HEADER ----------------

st.markdown("""
<div style="padding: 1rem 0">
    <div style="
        color:#a78bfa;
        text-transform:uppercase;
        letter-spacing:2px;
        font-size:.78rem;
        font-weight:800;">
        AI-ASSISTED PROJECT PLANNING
    </div>
    <div class="brand">EstiMate<span>Ai</span></div>
    <div class="tagline">Estimate Smarter, Build Better.</div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# OVERVIEW
# ==================================================

if page == "Overview":

    st.markdown("### Plan with clarity. Build with confidence.")

    st.write(
        "Estimate software project effort and budget "
        "using project scope, team details and resource costs."
    )

    c1, c2, c3 = st.columns(3)

    cards = [
        (c1, "PERSONNEL", "Role-based",
         "Development, testing and management"),
        (c2, "RESOURCES", "Included",
         "Cloud, tools and contingency"),
        (c3, "PLANNING", "Compare",
         "Explore different project scenarios")
    ]

    for col, label, value, sub in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    left, right = st.columns(2)

    with left:
        st.markdown("#### What EstiMateAi helps you do")
        st.markdown("""
        - Estimate software project costs.
        - Calculate personnel expenses.
        - Include cloud and tooling costs.
        - Compare alternative team sizes.
        - Explore historical project datasets.
        """)

    with right:
        st.markdown("#### How it works")
        st.markdown("""
        **01 — Describe:** Enter project details.

        **02 — Estimate:** Calculate effort and costs.

        **03 — Compare:** Review different scenarios.

        **04 — Improve:** Connect a trained ML model.
        """)

    st.info(
        "This prototype uses a demonstration formula. "
        "Its estimates are not trained-AI predictions."
    )


# ==================================================
# COST ESTIMATOR
# ==================================================

elif page == "Cost Estimator":

    st.markdown("### Project cost estimator")

    st.write(
        "Enter your project details and adjust the resource "
        "rates to match your assumptions."
    )

    with st.form("estimate_form"):

        a, b, c = st.columns(3)

        with a:
            project_name = st.text_input(
                "Project name", "Mobile App Project"
            )

            team_size = st.slider(
                "Team size", 1, 30, 5
            )

            experience = st.slider(
                "Average experience (years)", 0, 15, 3
            )

        with b:
            complexity = st.selectbox(
                "Project complexity",
                ["Low", "Medium", "High", "Very high"],
                index=2
            )

            features = st.slider(
                "Features / modules", 1, 100, 20
            )

            months = st.slider(
                "Expected duration (months)", 1, 36, 6
            )

        with c:
            dev_rate = st.number_input(
                "Developer cost (₹ / hour)",
                min_value=100, max_value=5000,
                value=600, step=50
            )

            tester_rate = st.number_input(
                "Tester cost (₹ / hour)",
                min_value=100, max_value=4000,
                value=400, step=50
            )

            manager_rate = st.number_input(
                "Manager cost (₹ / hour)",
                min_value=100, max_value=6000,
                value=800, step=50
            )

            cloud_monthly = st.number_input(
                "Cloud / infrastructure (₹ / month)",
                min_value=0, max_value=10000000,
                value=12000, step=1000
            )

            tools_monthly = st.number_input(
                "Tools / licenses (₹ / month)",
                min_value=0, max_value=10000000,
                value=5000, step=500
            )

        contingency_pct = st.slider(
            "Contingency buffer (%)", 0, 30, 10
        )

        submitted = st.form_submit_button(
            "Estimate project cost",
            use_container_width=True
        )

    if submitted:

        result = estimate_project(
            team_size,
            experience,
            complexity,
            features,
            months,
            dev_rate,
            tester_rate,
            manager_rate,
            cloud_monthly,
            tools_monthly,
            contingency_pct
        )

        st.session_state["last_result"] = result
        st.session_state["last_project"] = project_name

        st.session_state["last_inputs"] = {
            "Project": project_name,
            "Team size": team_size,
            "Experience (years)": experience,
            "Complexity": complexity,
            "Features": features,
            "Duration (months)": months
        }

    if "last_result" in st.session_state:

        r = st.session_state["last_result"]

        st.divider()

        st.markdown(
            f"### Estimate for "
            f"{st.session_state.get('last_project', 'Your project')}"
        )

        k1, k2, k3, k4 = st.columns(4)

        metrics = [
            (k1, "TOTAL ESTIMATED COST",
             money(r["total_cost"]), "Includes contingency"),
            (k2, "TOTAL EFFORT",
             f'{r["total_effort"]:,.0f} hrs', "Estimated person-hours"),
            (k3, "DURATION",
             f'{r["duration_months"]} months', "Entered duration"),
            (k4, "CONTINGENCY",
             money(r["contingency"]), "Risk buffer")
        ]

        for col, label, value, sub in metrics:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-sub">{sub}</div>
                </div>
                """, unsafe_allow_html=True)

        breakdown = pd.DataFrame({
            "Cost component": [
                "Personnel",
                "Cloud / infrastructure",
                "Tools / licenses",
                "Contingency"
            ],
            "Estimated cost": [
                r["personnel_cost"],
                r["cloud_cost"],
                r["tool_cost"],
                r["contingency"]
            ]
        })

        ch1, ch2 = st.columns(2)

        with ch1:
            st.markdown("#### Cost breakdown")
            display_breakdown = breakdown.copy()
            display_breakdown["Estimated cost"] = (
                display_breakdown["Estimated cost"].map(money)
            )
            st.dataframe(
                display_breakdown,
                use_container_width=True,
                hide_index=True
            )

        with ch2:
            fig = px.pie(
                breakdown,
                names="Cost component",
                values="Estimated cost",
                hole=0.58,
                color_discrete_sequence=[
                    "#8b5cf6", "#3b82f6",
                    "#a78bfa", "#64748b"
                ]
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#e8e7f4"
            )

            st.plotly_chart(fig, use_container_width=True)

        st.markdown("#### Effort by role")

        hours = pd.DataFrame({
            "Role": ["Development", "Testing", "Management"],
            "Estimated hours": [
                r["development_hours"],
                r["testing_hours"],
                r["management_hours"]
            ]
        })

        st.dataframe(
            hours.style.format({"Estimated hours": "{:,.0f}"}),
            use_container_width=True,
            hide_index=True
        )

        export = pd.DataFrame([{
            **st.session_state["last_inputs"],
            "Development hours": round(r["development_hours"]),
            "Testing hours": round(r["testing_hours"]),
            "Management hours": round(r["management_hours"]),
            "Personnel cost": round(r["personnel_cost"]),
            "Cloud cost": round(r["cloud_cost"]),
            "Tool/license cost": round(r["tool_cost"]),
            "Contingency": round(r["contingency"]),
            "Total estimated cost": round(r["total_cost"])
        }])

        st.download_button(
            "Download estimate as CSV",
            export.to_csv(index=False).encode("utf-8"),
            file_name="estimateai_project_estimate.csv",
            mime="text/csv"
        )


# ==================================================
# SCENARIO PLANNER
# ==================================================

elif page == "Scenario Planner":

    st.markdown("### Scenario planner")

    st.write(
        "Compare different team sizes while keeping other "
        "project assumptions consistent."
    )

    x1, x2, x3 = st.columns(3)

    with x1:
        complexity = st.selectbox(
            "Complexity",
            ["Low", "Medium", "High", "Very high"],
            index=2,
            key="sc_complexity"
        )

        experience = st.slider(
            "Average experience (years)",
            0, 15, 3, key="sc_experience"
        )

    with x2:
        features = st.slider(
            "Features / modules",
            1, 100, 20, key="sc_features"
        )

        months = st.slider(
            "Duration (months)",
            1, 36, 6, key="sc_months"
        )

    with x3:
        cloud = st.number_input(
            "Cloud cost / month (₹)",
            min_value=0, value=12000, step=1000,
            key="sc_cloud"
        )

        tools = st.number_input(
            "Tools / licenses / month (₹)",
            min_value=0, value=5000, step=500,
            key="sc_tools"
        )

    rows = []

    for team in [3, 5, 7, 10]:

        r = estimate_project(
            team, experience, complexity, features, months,
            600, 400, 800, cloud, tools, 10
        )

        rows.append({
            "Team size": team,
            "Estimated effort (hours)": round(r["total_effort"]),
            "Personnel cost (₹)": round(r["personnel_cost"]),
            "Total cost (₹)": round(r["total_cost"])
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.style.format({
            "Personnel cost (₹)": "₹{:,.0f}",
            "Total cost (₹)": "₹{:,.0f}",
            "Estimated effort (hours)": "{:,.0f}"
        }),
        use_container_width=True,
        hide_index=True
    )

    fig = px.bar(
        df,
        x="Team size",
        y="Total cost (₹)",
        color="Team size",
        title="Estimated cost by team size",
        color_discrete_sequence=[
            "#8b5cf6", "#6366f1", "#3b82f6", "#60a5fa"
        ]
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e8e7f4"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Illustrative scenario comparison. Duration is held constant."
    )


# ==================================================
# DATASET EXPLORER
# ==================================================

elif page == "Dataset Explorer":

    st.markdown("### Historical dataset explorer")

    st.write(
        "Upload a CSV file to inspect historical project data."
    )

    uploaded = st.file_uploader(
        "Upload project dataset",
        type=["csv"]
    )

    if uploaded is not None:

        try:
            data = pd.read_csv(uploaded)

            st.success(
                f"Loaded {len(data):,} rows and "
                f"{len(data.columns)} columns."
            )

            st.dataframe(
                data.head(100),
                use_container_width=True
            )

            numeric = data.select_dtypes(include=np.number)

            if not numeric.empty:

                st.markdown("#### Numeric summary")

                st.dataframe(
                    numeric.describe().T,
                    use_container_width=True
                )

                target = st.selectbox(
                    "Choose a numeric field to visualize",
                    numeric.columns.tolist()
                )

                fig = px.histogram(
                    data,
                    x=target,
                    nbins=25,
                    title=f"Distribution of {target}",
                    color_discrete_sequence=["#8b5cf6"]
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e8e7f4"
                )

                st.plotly_chart(fig, use_container_width=True)

            st.download_button(
                "Download uploaded CSV",
                data.to_csv(index=False).encode("utf-8"),
                file_name="dataset_copy.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Could not read this CSV: {e}")

    else:

        sample_path = Path(__file__).parent / "sample_projects.csv"

        if sample_path.exists():

            sample = pd.read_csv(sample_path)

            st.info("Showing the included sample dataset.")

            st.dataframe(
                sample.head(20),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download sample CSV",
                sample.to_csv(index=False).encode("utf-8"),
                file_name="estimateai_sample_projects.csv",
                mime="text/csv"
            )

        else:
            st.info(
                "Upload your project CSV to explore its contents."
            )

        st.caption(
            "Dataset exploration does not automatically train a model."
        )


# ==================================================
# ABOUT
# ==================================================

elif page == "About":

    st.markdown("### About EstiMateAi")

    st.write(
        "EstiMateAi is a project-planning prototype designed "
        "to support early software project cost estimation."
    )

    st.markdown("""
    **Tagline:** Estimate Smarter, Build Better.

    **Problem:** Software estimates can miss personnel,
    tooling and infrastructure expenses.

    **Features:** Cost estimation, role-level effort breakdown,
    cost visualization, scenario comparison and CSV exploration.

    **Next step:** Connect a trained regression model using
    validated historical project data.
    """)

    st.warning(
        "The current estimator uses a demonstration formula, "
        "not a trained AI model. Validate estimates against "
        "real project records before relying on them."
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "EstiMateAi • Estimate Smarter, Build Better • "
    "Prototype estimates are planning aids, not financial guarantees."
)
