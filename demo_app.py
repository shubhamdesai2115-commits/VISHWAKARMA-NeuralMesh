"""
VISHWAKARMA — Streamlit Demo App
Run: streamlit run demo_app.py
Judge-ready interactive prototype.
"""

import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.disrupt_radar import calculate_risk_score, get_affected_components
from modules.material_genome import find_substitute, rewrite_bom
from modules.supplier_pulse import get_supplier_health, get_at_risk_suppliers
from modules.niti_shield import predict_policy_risk
from modules.shopsense import monitor_cp_cpk

# ─── PAGE CONFIG ───────────────────────────────────────────
st.set_page_config(
    page_title="VISHWAKARMA — Supply Chain AI",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── SIDEBAR ───────────────────────────────────────────────
st.sidebar.image("https://img.shields.io/badge/VISHWAKARMA-v1.0-gold?style=for-the-badge")
st.sidebar.title("⚙ VISHWAKARMA")
st.sidebar.caption("AI Supply Chain Resilience Engine")
st.sidebar.markdown("---")
module = st.sidebar.radio(
    "Select Module",
    ["🏠 Overview", "⚡ DisruptRadar", "⚗ Material Genome",
     "📡 Supplier Pulse", "🛡 NITI Shield", "🔬 ShopSense"]
)
st.sidebar.markdown("---")
st.sidebar.caption("Team Takumi Type | COEP Tech, Pune")
st.sidebar.caption("ET AutoTech Hackathon 2026")

# ─── OVERVIEW ──────────────────────────────────────────────
if module == "🏠 Overview":
    st.title("⚙ VISHWAKARMA")
    st.subheader("India's Supply Chain Never Stops.")
    st.markdown("""
    > AI-Powered Supply Chain Resilience Engine for India's ₹18 Lakh Crore Automotive Industry
    """)

    col1, col2, col3 = st.columns(3)
    col1.metric("Annual OEM Savings", "₹47,000 Cr", "+15% efficiency")
    col2.metric("Jobs Protected", "37 Million", "Direct + indirect")
    col3.metric("China Dependency", "93% → 30%", "-63% in 5 years")

    st.markdown("---")
    st.subheader("5 AI Modules")
    cols = st.columns(5)
    modules_info = [
        ("⚡", "DisruptRadar", "Global risk scanning\n90-day predictions"),
        ("⚗", "Material Genome", "Shortage → Substitute\nBOM auto-rewrite"),
        ("📡", "Supplier Pulse", "MSME-level\ninsolvency warning"),
        ("🛡", "NITI Shield", "Policy prediction\n90 days advance"),
        ("🔬", "ShopSense", "CV defect detection\nCp/Cpk monitoring"),
    ]
    for col, (icon, name, desc) in zip(cols, modules_info):
        col.info(f"**{icon} {name}**\n\n{desc}")

# ─── DISRUPTRADAR ──────────────────────────────────────────
elif module == "⚡ DisruptRadar":
    st.title("⚡ DisruptRadar")
    st.caption("30/60/90-day disruption probability scores for automotive components")

    component = st.selectbox(
        "Select Component",
        ["NdFeB permanent magnet", "Dysprosium", "Semiconductor chip",
         "Lithium battery cell", "Cobalt cathode", "Palladium catalyst"]
    )

    if st.button("Calculate Risk Score", type="primary"):
        with st.spinner("Analysing global signals..."):
            result = calculate_risk_score(component)

        scores = result["risk_scores"]
        status = scores["status"]

        color = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(status, "⚪")
        st.markdown(f"### {color} Risk Status: **{status}**")

        col1, col2, col3 = st.columns(3)
        col1.metric("30-Day Risk", f"{scores['30d']}%")
        col2.metric("60-Day Risk", f"{scores['60d']}%")
        col3.metric("90-Day Risk", f"{scores['90d']}%")

        st.info(f"**Recommended Action:** {result['recommended_action']}")
        st.write("**Affected Vehicle Models:**", ", ".join(result["affected_vehicle_models"]))

    st.markdown("---")
    st.subheader("All High-Risk Components")
    affected = get_affected_components()
    if affected["critical"]:
        st.error(f"**CRITICAL:** {', '.join(c['component'] for c in affected['critical'])}")
    if affected["high"]:
        st.warning(f"**HIGH:** {', '.join(c['component'] for c in affected['high'])}")

# ─── MATERIAL GENOME ───────────────────────────────────────
elif module == "⚗ Material Genome":
    st.title("⚗ Material Genome Engine")
    st.caption("World's first AI material substitution + BOM auto-rewrite system")

    col1, col2 = st.columns(2)
    with col1:
        material_name = st.text_input("Shortage Material", value="NdFeB Permanent Magnet N42")
        properties = st.text_area(
            "Material Properties",
            value="Remanence 1.4T Coercivity 1000kA/m Max Energy Product 350kJ/m3 density 7500kg/m3",
            height=100
        )
        quantity = st.number_input("Required Quantity (units)", value=1000, min_value=1)

    with col2:
        st.info("**How it works:**\n\n"
                "1. Enter shortage material properties\n"
                "2. AI searches 4,200+ Indian domestic materials\n"
                "3. FAISS vector search finds closest property match\n"
                "4. Returns supplier, stock, cost delta in <60 seconds")

    if st.button("Find Substitute", type="primary"):
        with st.spinner("Searching Material Genome Database..."):
            result = find_substitute(material_name, properties, quantity)

        st.success(f"**Best Match: {result['recommended']['material']}**")

        rec = result["recommended"]
        cols = st.columns(4)
        cols[0].metric("Supplier", rec["supplier"].split(",")[0])
        cols[1].metric("Cost Delta", rec["cost_delta_percent"])
        cols[2].metric("Lead Time", f"{rec['lead_time_days']} days")
        cols[3].metric("Action", "✅ PROCEED")

        st.write("**Machine Compatible With:**", ", ".join(rec["machine_compatible"]))
        st.write("**Location:**", rec["location"])

        st.markdown("#### Top 3 Substitutes")
        for sub in result["top_substitutes"]:
            st.write(f"**Rank {sub['rank']}:** {sub['material']} — "
                     f"Match: {sub['match_score']}% | "
                     f"Stock: {'✅' if sub['stock_available'] else '❌'} | "
                     f"₹{sub['price_per_kg']}/kg")

# ─── SUPPLIER PULSE ────────────────────────────────────────
elif module == "📡 Supplier Pulse":
    st.title("📡 Supplier Pulse")
    st.caption("India's first MSME-level supply chain AI — 60-day insolvency warning")

    st.subheader("At-Risk Suppliers Dashboard")
    at_risk = get_at_risk_suppliers()
    st.error(at_risk["alert"])

    for sup in at_risk["at_risk_suppliers"]:
        color = "🔴" if sup["health_score"] < 35 else "🟠" if sup["health_score"] < 55 else "🟡"
        with st.expander(f"{color} {sup['name']} — Health Score: {sup['health_score']}/100 (Tier {sup['tier']})"):
            detail = get_supplier_health(sup["supplier_id"])
            st.write("**Warning Signals:**")
            for sig in detail.get("warning_signals", []):
                st.write(f"  ⚠ {sig}")
            st.info(f"**Action:** {detail.get('recommended_action', '')}")
            st.write("**Alternate Suppliers:**")
            for alt in detail.get("alternate_suppliers", []):
                st.write(f"  → {alt}")

# ─── NITI SHIELD ───────────────────────────────────────────
elif module == "🛡 NITI Shield":
    st.title("🛡 NITI Shield")
    st.caption("Trade policy prediction — 60-90 days before official announcement")

    country = st.selectbox("Select Country", ["China", "USA", "Russia"])

    if st.button("Analyse Policy Risk", type="primary"):
        with st.spinner("Scanning parliamentary signals, WTO filings..."):
            result = predict_policy_risk(country)

        risk_color = "🔴" if result["overall_risk"] == "CRITICAL" else "🟠"
        st.markdown(f"### {risk_color} Overall Risk: **{result['overall_risk']}**")
        st.write(result["summary"])

        for policy in result.get("high_risk_policies", []):
            with st.expander(f"🔴 {policy['policy_type']} — Signal: {policy['signal_strength']}/100"):
                st.write(f"**Prediction:** {policy['prediction']}")
                st.write(f"**Affected Materials:** {', '.join(policy['affected_materials'])}")
                st.write(f"**Parliament Mentions (90d):** {policy['parliament_mentions_last_90d']}")
                st.info(f"**Action:** {policy['action']}")

        st.markdown("#### India Domestic Policy Watch")
        for item in result.get("india_domestic_watch", []):
            st.write(f"**{item['policy']}** — {item['status']}")
            st.caption(f"Impact: {item['impact']}")

# ─── SHOPSENSE ─────────────────────────────────────────────
elif module == "🔬 ShopSense":
    st.title("🔬 ShopSense")
    st.caption("Real-time shop floor AI — Cp/Cpk monitoring + defect detection")

    st.subheader("Process Capability Calculator (Cp / Cpk)")

    col1, col2, col3 = st.columns(3)
    with col1:
        process_name = st.text_input("Process Name", value="Motor shaft diameter")
        usl = st.number_input("Upper Spec Limit (USL)", value=25.05)
        lsl = st.number_input("Lower Spec Limit (LSL)", value=24.95)

    with col2:
        st.write("**Enter Measurements (one per line)**")
        raw = st.text_area("Measurements", value="25.01\n25.03\n24.99\n25.02\n25.00\n25.04\n24.98\n25.01\n25.03\n25.00", height=180)

    with col3:
        st.info("**Automotive Benchmark:**\n\n"
                "Cpk ≥ 1.67 — Excellent\n"
                "Cpk ≥ 1.33 — PASS (IATF 16949)\n"
                "Cpk ≥ 1.00 — Marginal\n"
                "Cpk < 1.00 — STOP LINE")

    if st.button("Calculate Cp / Cpk", type="primary"):
        try:
            measurements = [float(x.strip()) for x in raw.strip().split("\n") if x.strip()]
            result = monitor_cp_cpk(measurements, usl, lsl, process_name)

            cpk = result["capability_indices"]["Cpk"]
            cp  = result["capability_indices"]["Cp"]

            cols = st.columns(4)
            cols[0].metric("Cp",  cp)
            cols[1].metric("Cpk", cpk)
            cols[2].metric("Within Spec", f"{result['within_spec_percent']}%")
            cols[3].metric("Out of Spec", result['out_of_spec_count'])

            if result["alert"]:
                st.error(f"⚠ DRIFT ALERT: {result['status']}")
            else:
                st.success(f"✅ {result['status']}")

            st.info(f"**Recommended Action:** {result['recommended_action']}")

        except ValueError:
            st.error("Please enter valid numeric measurements, one per line.")
