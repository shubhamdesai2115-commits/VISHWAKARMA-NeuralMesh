"""
VISHWAKARMA — AI Supply Chain Resilience Engine
ET AutoTech Hackathon 2026 | Team Takumi Type
Shubham Pravin Desai | COEP Technological University, Pune
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from modules.disrupt_radar import calculate_risk_score, get_affected_components
from modules.material_genome import find_substitute, rewrite_bom
from modules.supplier_pulse import get_supplier_health, get_at_risk_suppliers
from modules.niti_shield import predict_policy_risk
from modules.shopsense import detect_defects_from_path, monitor_cp_cpk

app = FastAPI(
    title="VISHWAKARMA API",
    description="AI-Powered Supply Chain Resilience Engine for India's Automotive Industry",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── REQUEST MODELS ────────────────────────────────────────

class SubstituteRequest(BaseModel):
    material_name: str
    properties: str
    quantity: Optional[int] = 1000

class BOMRequest(BaseModel):
    original_material: str
    substitute_material: str
    bom_items: list

class CPKRequest(BaseModel):
    measurements: list
    usl: float
    lsl: float
    process_name: str

# ─── HEALTH CHECK ──────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    return {
        "system": "VISHWAKARMA",
        "status": "OPERATIONAL",
        "modules": ["DisruptRadar", "MaterialGenome", "SupplierPulse", "NITIShield", "ShopSense"],
        "team": "Team Takumi Type | COEP Technological University"
    }

# ─── MODULE 01: DISRUPTRADAR ───────────────────────────────

@app.get("/api/v1/disrupt/risk/{component}", tags=["DisruptRadar"])
async def get_risk(component: str):
    """Get 30/60/90-day disruption risk score for any component."""
    try:
        result = calculate_risk_score(component)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/disrupt/affected", tags=["DisruptRadar"])
async def affected_components():
    """Get all components currently at high disruption risk."""
    return get_affected_components()

# ─── MODULE 02: MATERIAL GENOME ────────────────────────────

@app.post("/api/v1/genome/substitute", tags=["MaterialGenome"])
async def get_material_substitute(req: SubstituteRequest):
    """Find best Indian domestic substitute for a shortage material."""
    try:
        result = find_substitute(req.material_name, req.properties, req.quantity)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/genome/rewrite-bom", tags=["MaterialGenome"])
async def rewrite_bom_endpoint(req: BOMRequest):
    """Auto-rewrite BOM with substitute material and cost delta."""
    try:
        result = rewrite_bom(req.original_material, req.substitute_material, req.bom_items)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── MODULE 03: SUPPLIER PULSE ─────────────────────────────

@app.get("/api/v1/supplier/health/{supplier_id}", tags=["SupplierPulse"])
async def supplier_health(supplier_id: str):
    """Get real-time financial health score for a Tier-2/3 supplier."""
    try:
        return get_supplier_health(supplier_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/supplier/at-risk", tags=["SupplierPulse"])
async def at_risk_suppliers():
    """List all suppliers with health score below safe threshold."""
    return get_at_risk_suppliers()

# ─── MODULE 04: NITI SHIELD ────────────────────────────────

@app.get("/api/v1/policy/risk/{country}", tags=["NITIShield"])
async def policy_risk(country: str):
    """Predict trade policy risk for a country 60-90 days in advance."""
    try:
        return predict_policy_risk(country)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ─── MODULE 05: SHOPSENSE ──────────────────────────────────

@app.post("/api/v1/shop/cpk", tags=["ShopSense"])
async def cpk_analysis(req: CPKRequest):
    """Calculate Cp/Cpk process capability and return drift alerts."""
    try:
        return monitor_cp_cpk(req.measurements, req.usl, req.lsl, req.process_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
