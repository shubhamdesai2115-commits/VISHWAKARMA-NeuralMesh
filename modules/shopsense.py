"""
MODULE 05 — ShopSense
Real-time shop floor AI during material changeover.
CV defect detection + Cp/Cpk process capability monitoring
+ AI-guided operator instructions.
"""

import numpy as np
from datetime import datetime
from typing import Optional


def detect_defects_from_path(image_path: str) -> dict:
    """
    Run YOLOv8 defect detection on a shop floor image.
    In production: connected to line camera feed via RTSP stream.
    For demo: runs on uploaded image file.
    """
    try:
        from ultralytics import YOLO
        import cv2

        model = YOLO("yolov8n.pt")
        frame = cv2.imread(image_path)
        if frame is None:
            return {"error": "Could not read image", "path": image_path}

        results = model(frame, verbose=False)
        boxes = results[0].boxes

        defects_detected = []
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                if float(box.conf[0]) > 0.60:
                    defects_detected.append({
                        "confidence": round(float(box.conf[0]), 3),
                        "class": results[0].names[int(box.cls[0])],
                        "bbox": box.xyxy[0].tolist()
                    })

        pass_qc = len(defects_detected) == 0

        return {
            "image_path": image_path,
            "defects_detected": len(defects_detected),
            "defect_details": defects_detected,
            "qc_result": "PASS ✓" if pass_qc else "FAIL ✗",
            "action": "Continue production" if pass_qc else "STOP LINE — Flag unit for rework",
            "timestamp": datetime.now().isoformat()
        }

    except ImportError:
        # Demo fallback when ultralytics not installed
        return _demo_defect_result(image_path)


def _demo_defect_result(image_path: str) -> dict:
    """Demo result for environments without ultralytics."""
    return {
        "image_path": image_path,
        "defects_detected": 0,
        "defect_details": [],
        "qc_result": "PASS ✓",
        "action": "Continue production",
        "note": "Demo mode — install ultralytics for live detection",
        "timestamp": datetime.now().isoformat()
    }


def monitor_cp_cpk(
    measurements: list,
    usl: float,
    lsl: float,
    process_name: str,
    target: Optional[float] = None
) -> dict:
    """
    Calculate Cp, Cpk, and Cpm process capability indices.
    Alert if Cpk drops below 1.33 (industry standard for automotive).
    """
    if len(measurements) < 5:
        return {"error": "Minimum 5 measurements required for Cp/Cpk calculation"}

    data = np.array(measurements, dtype=float)
    mean = float(np.mean(data))
    std  = float(np.std(data, ddof=1))  # sample std dev

    if std == 0:
        return {"error": "Zero standard deviation — all measurements identical"}

    cp   = round((usl - lsl) / (6 * std), 4)
    cpu  = round((usl - mean) / (3 * std), 4)
    cpl  = round((mean - lsl) / (3 * std), 4)
    cpk  = round(min(cpu, cpl), 4)

    # Cpm (Taguchi capability) — requires target
    cpm = None
    if target is not None:
        tau = np.sqrt(std**2 + (mean - target)**2)
        cpm = round((usl - lsl) / (6 * float(tau)), 4)

    # Out of spec count
    out_of_spec = int(np.sum((data < lsl) | (data > usl)))
    within_spec_pct = round(((len(data) - out_of_spec) / len(data)) * 100, 2)

    # Determine status
    if cpk >= 1.67:   status = "EXCELLENT — Six Sigma capable"
    elif cpk >= 1.33: status = "PASS — Automotive grade (IATF 16949 compliant)"
    elif cpk >= 1.00: status = "MARGINAL — Improvement needed"
    elif cpk >= 0.67: status = "POOR — Process out of control"
    else:             status = "CRITICAL — STOP PRODUCTION"

    alert = cpk < 1.33

    # AI-guided action
    action = _get_cpk_action(cpk, mean, usl, lsl, process_name)

    return {
        "process_name": process_name,
        "sample_size": len(measurements),
        "statistics": {
            "mean":    round(mean, 4),
            "std_dev": round(std, 4),
            "min":     round(float(np.min(data)), 4),
            "max":     round(float(np.max(data)), 4),
            "usl": usl,
            "lsl": lsl,
        },
        "capability_indices": {
            "Cp":  cp,
            "Cpu": cpu,
            "Cpl": cpl,
            "Cpk": cpk,
            "Cpm": cpm,
        },
        "out_of_spec_count": out_of_spec,
        "within_spec_percent": within_spec_pct,
        "status": status,
        "alert": alert,
        "recommended_action": action,
        "timestamp": datetime.now().isoformat()
    }


def get_changeover_guidance(
    original_material: str,
    new_material: str,
    process_type: str
) -> dict:
    """
    Return step-by-step operator guidance for material changeover.
    Covers machine settings, QC checkpoints, first-article inspection.
    """
    guidance_db = {
        ("NdFeB", "Ferrite", "motor_assembly"): {
            "steps": [
                "1. STOP magnetizing station. Lock out/tag out (LOTO).",
                "2. Replace magnetizer fixture — Ferrite Y30 requires 15% higher field strength.",
                "3. Adjust magnetizing cycle time: +8 seconds per unit.",
                "4. Update torque spec on assembly card: reduce target by 8% (flux density difference).",
                "5. Run 10-unit first-article inspection. Measure back-EMF at 1000 RPM.",
                "6. If back-EMF within ±5% of baseline: PROCEED to full production.",
                "7. Update BOM traveller card with new material code: MAT001-Y30.",
                "8. Inform QC supervisor — update control plan revision.",
            ],
            "estimated_changeover_time_min": 45,
            "first_article_units": 10,
            "critical_checks": ["Back-EMF", "Holding torque", "Air gap measurement"],
        },
        ("NdFeB", "AlNiCo", "motor_assembly"): {
            "steps": [
                "1. LOTO magnetizing station.",
                "2. AlNiCo Grade 5 — compatible with existing magnetizer (field strength PASS).",
                "3. Cycle time unchanged.",
                "4. Monitor for demagnetization above 450°C — update thermal limit alarm.",
                "5. Run 5-unit first-article inspection.",
                "6. Update BOM traveller: MAT002-ALNICO5.",
            ],
            "estimated_changeover_time_min": 25,
            "first_article_units": 5,
            "critical_checks": ["Holding torque", "Thermal demagnetization test"],
        },
    }

    # Find matching guidance
    for (orig, new, proc), guide in guidance_db.items():
        if orig.lower() in original_material.lower() and \
           new.lower() in new_material.lower() and \
           proc.lower() in process_type.lower():
            return {
                "original_material": original_material,
                "new_material": new_material,
                "process": process_type,
                "changeover_steps": guide["steps"],
                "estimated_changeover_time_min": guide["estimated_changeover_time_min"],
                "first_article_units": guide["first_article_units"],
                "critical_checks": guide["critical_checks"],
                "safety_note": "Always follow LOTO procedure before any fixture change.",
                "timestamp": datetime.now().isoformat()
            }

    # Generic fallback
    return {
        "original_material": original_material,
        "new_material": new_material,
        "process": process_type,
        "changeover_steps": [
            "1. Review material data sheet for new material.",
            "2. Verify dimensional compatibility with existing tooling.",
            "3. Adjust process parameters per material supplier recommendations.",
            "4. Run first-article inspection (min 10 units).",
            "5. Update BOM and control plan.",
            "6. Inform QC and production supervisor.",
        ],
        "note": "Specific guidance not yet programmed — contact process engineering.",
        "timestamp": datetime.now().isoformat()
    }


def _get_cpk_action(cpk: float, mean: float, usl: float, lsl: float, process: str) -> str:
    if cpk >= 1.33:
        return "Process in control. Continue production. Monitor at standard frequency."
    if cpk >= 1.00:
        mid = (usl + lsl) / 2
        direction = "INCREASE" if mean < mid else "DECREASE"
        return (f"Process marginal. {direction} {process} parameter by 5% to centre distribution. "
                f"Re-measure after 20 units.")
    if cpk >= 0.67:
        return (f"Process out of control. REDUCE variation immediately. "
                f"Check tooling wear, fixture clamping, material batch consistency.")
    return (f"CRITICAL: STOP PRODUCTION on {process}. "
            f"Root cause analysis required before restart. Tag all suspect units.")
