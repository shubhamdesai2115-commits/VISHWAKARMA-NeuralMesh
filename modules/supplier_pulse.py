"""
MODULE 03 — Supplier Pulse
India's first MSME-level supply chain AI.
Tracks non-financial signals (GST gaps, electricity, hiring) to
predict Tier-2/3 supplier insolvency 60-90 days in advance.
"""

import random
from datetime import datetime, timedelta
from typing import Optional

# ─── MOCK SUPPLIER DATABASE ────────────────────────────────
# In production: connected to MCA21, GST portal, LinkedIn, MSME Samridhi

SUPPLIER_DB = {
    "SUP001": {
        "name": "Precision Auto Components Pvt Ltd",
        "location": "Pune, Maharashtra",
        "tier": 2,
        "category": "Stampings & Forgings",
        "annual_turnover_cr": 42,
        "employees": 180,
        "signals": {
            "gst_filing_delay_days": 67,
            "electricity_consumption_drop_pct": 38,
            "job_postings_change_pct": -72,
            "epf_payment_delay_days": 22,
            "bank_account_activity": "DECLINING",
            "last_order_fulfilled": "On time",
        }
    },
    "SUP002": {
        "name": "Shree Ganesh Rubber Industries",
        "location": "Aurangabad, Maharashtra",
        "tier": 3,
        "category": "Seals & Gaskets",
        "annual_turnover_cr": 8,
        "employees": 45,
        "signals": {
            "gst_filing_delay_days": 12,
            "electricity_consumption_drop_pct": 5,
            "job_postings_change_pct": 8,
            "epf_payment_delay_days": 0,
            "bank_account_activity": "STABLE",
            "last_order_fulfilled": "On time",
        }
    },
    "SUP003": {
        "name": "Bharat Electrical Works",
        "location": "Coimbatore, Tamil Nadu",
        "tier": 2,
        "category": "Wiring Harness",
        "annual_turnover_cr": 28,
        "employees": 220,
        "signals": {
            "gst_filing_delay_days": 95,
            "electricity_consumption_drop_pct": 51,
            "job_postings_change_pct": -89,
            "epf_payment_delay_days": 45,
            "bank_account_activity": "CRITICAL",
            "last_order_fulfilled": "Delayed 12 days",
        }
    },
    "SUP004": {
        "name": "Indo Cast Alloys Ltd",
        "location": "Rajkot, Gujarat",
        "tier": 2,
        "category": "Die Castings",
        "annual_turnover_cr": 65,
        "employees": 310,
        "signals": {
            "gst_filing_delay_days": 8,
            "electricity_consumption_drop_pct": -2,
            "job_postings_change_pct": 15,
            "epf_payment_delay_days": 0,
            "bank_account_activity": "HEALTHY",
            "last_order_fulfilled": "On time",
        }
    },
}


def calculate_health_score(signals: dict) -> tuple:
    """
    Compute a 0-100 health score from non-financial signals.
    Lower = worse financial health.
    """
    score = 100.0

    # GST filing delay (max deduction: 35 points)
    gst_days = signals.get("gst_filing_delay_days", 0)
    if gst_days > 90:   score -= 35
    elif gst_days > 60: score -= 25
    elif gst_days > 30: score -= 15
    elif gst_days > 15: score -= 5

    # Electricity consumption drop (max deduction: 25 points)
    elec_drop = signals.get("electricity_consumption_drop_pct", 0)
    if elec_drop > 40:   score -= 25
    elif elec_drop > 25: score -= 18
    elif elec_drop > 10: score -= 8

    # Job postings decline (max deduction: 20 points)
    job_change = signals.get("job_postings_change_pct", 0)
    if job_change < -75:  score -= 20
    elif job_change < -50: score -= 14
    elif job_change < -25: score -= 8

    # EPF payment delay (max deduction: 15 points)
    epf_days = signals.get("epf_payment_delay_days", 0)
    if epf_days > 30:   score -= 15
    elif epf_days > 15: score -= 8
    elif epf_days > 5:  score -= 3

    # Bank activity
    bank = signals.get("bank_account_activity", "STABLE")
    if bank == "CRITICAL":   score -= 10
    elif bank == "DECLINING": score -= 5

    score = max(0.0, round(score, 1))

    if score < 35:   risk = "CRITICAL — Insolvency likely within 60 days"
    elif score < 55: risk = "HIGH — Insolvency possible within 90 days"
    elif score < 70: risk = "MEDIUM — Monitor closely"
    else:            risk = "LOW — Healthy"

    return score, risk


def get_supplier_health(supplier_id: str) -> dict:
    """Return health score and risk signals for a specific supplier."""
    if supplier_id not in SUPPLIER_DB:
        # Generate a plausible response for unknown IDs
        return {
            "supplier_id": supplier_id,
            "status": "NOT_IN_DATABASE",
            "message": "Supplier not yet indexed. Submit GST number for onboarding.",
            "timestamp": datetime.now().isoformat()
        }

    sup = SUPPLIER_DB[supplier_id]
    score, risk = calculate_health_score(sup["signals"])

    warning_signals = []
    s = sup["signals"]
    if s["gst_filing_delay_days"] > 30:
        warning_signals.append(f"GST filing delayed {s['gst_filing_delay_days']} days")
    if s["electricity_consumption_drop_pct"] > 10:
        warning_signals.append(f"Electricity consumption down {s['electricity_consumption_drop_pct']}%")
    if s["job_postings_change_pct"] < -25:
        warning_signals.append(f"Job postings declined {abs(s['job_postings_change_pct'])}%")
    if s["epf_payment_delay_days"] > 5:
        warning_signals.append(f"EPF payment delayed {s['epf_payment_delay_days']} days")
    if s["bank_account_activity"] in ["DECLINING", "CRITICAL"]:
        warning_signals.append(f"Bank account activity: {s['bank_account_activity']}")

    action = _get_procurement_action(score)

    return {
        "supplier_id": supplier_id,
        "supplier_name": sup["name"],
        "location": sup["location"],
        "tier": sup["tier"],
        "category": sup["category"],
        "health_score": score,
        "risk_assessment": risk,
        "warning_signals": warning_signals,
        "signals_count": len(warning_signals),
        "recommended_action": action,
        "alternate_suppliers": _get_alternates(sup["category"]),
        "timestamp": datetime.now().isoformat()
    }


def get_at_risk_suppliers() -> dict:
    """Return all suppliers below safe health threshold."""
    at_risk = []
    healthy = []

    for sup_id, sup_data in SUPPLIER_DB.items():
        score, risk = calculate_health_score(sup_data["signals"])
        entry = {
            "supplier_id": sup_id,
            "name": sup_data["name"],
            "tier": sup_data["tier"],
            "health_score": score,
            "risk": risk.split("—")[0].strip()
        }
        if score < 70:
            at_risk.append(entry)
        else:
            healthy.append(entry)

    at_risk.sort(key=lambda x: x["health_score"])

    return {
        "at_risk_count": len(at_risk),
        "healthy_count": len(healthy),
        "at_risk_suppliers": at_risk,
        "alert": f"ALERT: {len(at_risk)} suppliers require immediate procurement review",
        "timestamp": datetime.now().isoformat()
    }


def _get_procurement_action(score: float) -> str:
    if score < 35:
        return ("CRITICAL: Immediately qualify alternate supplier. "
                "Increase safety stock to 90 days. Escalate to supply chain head.")
    if score < 55:
        return ("URGENT: Contact supplier for business continuity plan. "
                "Identify backup supplier within 2 weeks.")
    if score < 70:
        return "MONITOR: Schedule quarterly review. Request updated financials."
    return "ROUTINE: Continue standard monitoring."


def _get_alternates(category: str) -> list:
    alternates_map = {
        "Stampings & Forgings": ["Bharat Forge Ltd — Pune", "Ramkrishna Forgings — Jamshedpur"],
        "Seals & Gaskets":      ["Parker Hannifin India — Chennai", "Freudenberg India — Pune"],
        "Wiring Harness":       ["Sumitomo Electric India — Chennai", "Motherson Sumi — Noida"],
        "Die Castings":         ["Endurance Technologies — Aurangabad", "Minda Industries — Pune"],
    }
    return alternates_map.get(category, ["Contact sourcing team for alternate supplier list"])
