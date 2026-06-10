# ⚙ VISHWAKARMA
### AI-Powered Supply Chain Resilience Engine
**ET AutoTech Hackathon 2026 | Team Takumi Type**

> *India's Supply Chain Never Stops.*

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-teal?style=flat-square)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## The Problem

India's automotive industry — worth ₹18 Lakh Crore — sources **93% of rare earth materials from China**. A single export restriction leaves Indian OEMs with only **2–3 weeks of stock**. 37 million livelihoods are at risk. No domestic intelligence or response system exists.

## The Solution

VISHWAKARMA is a 5-module AI platform that detects supply chain threats before they escalate and autonomously identifies Indian domestic alternatives — going from disruption signal to actionable BOM rewrite in under 60 seconds.

---

## 5 Modules

| Module | What It Does |
|--------|-------------|
| ⚡ **DisruptRadar** | Scans global news, commodity prices, trade signals. Generates 30/60/90-day disruption probability scores. |
| ⚗ **Material Genome** | Maps shortage material properties to Indian domestic substitutes using FAISS vector search. Auto-rewrites BOM. |
| 📡 **Supplier Pulse** | Tracks non-financial signals (GST gaps, electricity drops, hiring declines) to predict Tier-2/3 insolvency 60 days in advance. |
| 🛡 **NITI Shield** | Analyses parliamentary debates, WTO filings, and ministry press releases to predict trade policy changes 90 days before announcement. |
| 🔬 **ShopSense** | YOLOv8 defect detection + Cp/Cpk process capability monitoring + AI-guided operator instructions during material changeover. |

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/VISHWAKARMA-ET-AutoTech-2026.git
cd VISHWAKARMA-ET-AutoTech-2026

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the API
uvicorn main:app --reload
# API live at: http://localhost:8000
# Swagger docs: http://localhost:8000/docs

# 4. Run the demo app
streamlit run demo_app.py
# Demo live at: http://localhost:8501
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/disrupt/risk/{component}` | Disruption risk score for any component |
| GET | `/api/v1/disrupt/affected` | All components at HIGH/CRITICAL risk |
| POST | `/api/v1/genome/substitute` | Find Indian domestic substitute |
| POST | `/api/v1/genome/rewrite-bom` | Auto-rewrite BOM with substitute |
| GET | `/api/v1/supplier/health/{id}` | Supplier financial health score |
| GET | `/api/v1/supplier/at-risk` | All at-risk suppliers |
| GET | `/api/v1/policy/risk/{country}` | Trade policy risk prediction |
| POST | `/api/v1/shop/cpk` | Cp/Cpk process capability |

Full Swagger UI available at `/docs` when running locally.

---

## Example API Call

```bash
# Get risk score for NdFeB magnet
curl http://localhost:8000/api/v1/disrupt/risk/NdFeB%20permanent%20magnet

# Response:
{
  "component": "NdFeB permanent magnet",
  "risk_scores": {"30d": 94, "60d": 88, "90d": 82, "status": "CRITICAL"},
  "recommended_action": "IMMEDIATE: Trigger Material Genome Engine...",
  "affected_vehicle_models": ["Tata Nexon EV", "MG ZS EV", "Hyundai Ioniq"]
}
```

```bash
# Find domestic substitute
curl -X POST http://localhost:8000/api/v1/genome/substitute \
  -H "Content-Type: application/json" \
  -d '{"material_name": "NdFeB N42", "properties": "Remanence 1.4T Coercivity 1000kA/m", "quantity": 1000}'

# Response:
{
  "recommended": {
    "material": "Ferrite Grade Y30",
    "supplier": "TNPSC Magnetics Pvt Ltd",
    "location": "Chennai, Tamil Nadu",
    "cost_delta_percent": "-12%",
    "lead_time_days": 5
  }
}
```

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| AI / ML | Python 3.11, XGBoost, HuggingFace Transformers, FAISS, YOLOv8 |
| LLM APIs | OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet |
| Backend | FastAPI, PostgreSQL, Neo4j, Apache Kafka, Redis |
| Frontend | React.js 18, TailwindCSS, D3.js, Streamlit |
| Infra | Docker, Kubernetes, GitHub Actions CI/CD |
| Data | DGFT APIs, MCX feed, NewsAPI, GDELT, MCA21 GST |

---

## Project Structure

```
VISHWAKARMA/
├── main.py                  ← FastAPI application + all endpoints
├── demo_app.py              ← Streamlit interactive demo
├── requirements.txt         ← All dependencies
├── modules/
│   ├── disrupt_radar.py     ← MODULE 01: Risk scoring engine
│   ├── material_genome.py   ← MODULE 02: Substitution + BOM rewrite
│   ├── supplier_pulse.py    ← MODULE 03: MSME insolvency predictor
│   ├── niti_shield.py       ← MODULE 04: Policy prediction AI
│   └── shopsense.py         ← MODULE 05: CV defect + Cp/Cpk
└── README.md
```

---

## Impact

| Metric | Value |
|--------|-------|
| Annual savings for Indian OEMs | ₹47,000 Crore |
| Jobs protected | 37 Million |
| China rare earth dependency | 93% → 30% (5-year target) |
| Time from alert to BOM rewrite | < 60 seconds |
| Indian domestic materials indexed | 4,200+ |

---

## Team

**Shubham Pravin Desai**
B.Tech Mechanical Engineering — COEP Technological University, Pune

---

## License

MIT License — Open source, free to use and extend.

---

*Built for India. Built for 2026. Built to last until 2040.*
