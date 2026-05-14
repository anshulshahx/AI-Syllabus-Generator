import requests
import json
import os
from datetime import datetime
from app.config import OLLAMA_BASE_URL, OLLAMA_MODEL
from app.prompts.peo_prompt import build_peo_prompt, build_po_prompt, build_pso_prompt
from app.schemas.programme_models import (
    PEORequest, PEOResponse, PEOObject,
    PORequest, POResponse, POObject,
    PSORequest, PSOResponse, PSOObject,
    ProgrammeRequest, ProgrammeResponse
)

OUTPUTS_DIR = "outputs"

def call_ollama(prompt: str, timeout: int = 180) -> dict:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/generate",
        json={
            "model":  OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        },
        timeout=timeout
    )
    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    raw  = response.json()
    text = raw.get("response", "").strip()

    if "```" in text:
        for part in text.split("```"):
            if "{" in part:
                text = part.lstrip("json").strip()
                break

    return json.loads(text.strip())

def save_output(data: dict, prefix: str, name: str):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_")
    filename  = f"{OUTPUTS_DIR}/{prefix}_{safe_name}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved to {filename}")

# ── PEO Generator ────────────────────────────────────────────────
def generate_peos(request: PEORequest) -> PEOResponse:
    print(f"\nGenerating {request.n_peos} PEOs for {request.programme_name}")
    try:
        prompt = build_peo_prompt(
            request.programme_name,
            request.programme_description,
            request.n_peos
        )
        parsed = call_ollama(prompt)
        peos   = []

        for item in parsed.get("peos", []):
            peos.append(PEOObject(
                peo_id     = item.get("peo_id", f"PEO{len(peos)+1}"),
                text       = item.get("text", ""),
                focus_area = item.get("focus_area", "General")
            ))

        print(f"Generated {len(peos)} PEOs")
        save_output(
            {"programme": request.programme_name, "peos": [p.dict() for p in peos]},
            "peos", request.programme_name
        )
        return PEOResponse(programme_name=request.programme_name, peos=peos)

    except Exception as e:
        print(f"Error generating PEOs: {e}")
        return PEOResponse(programme_name=request.programme_name, peos=[])

# ── PO Generator ─────────────────────────────────────────────────
def generate_pos(request: PORequest) -> POResponse:
    print(f"\nGenerating standard 12 POs for {request.programme_name}")
    try:
        prompt = build_po_prompt(
            request.programme_name,
            request.programme_description
        )
        parsed = call_ollama(prompt)
        pos    = []

        for item in parsed.get("pos", []):
            pos.append(POObject(
                po_id = item.get("po_id", f"PO{len(pos)+1}"),
                title = item.get("title", ""),
                text  = item.get("text",  "")
            ))

        print(f"Generated {len(pos)} POs")
        save_output(
            {"programme": request.programme_name, "pos": [p.dict() for p in pos]},
            "pos", request.programme_name
        )
        return POResponse(programme_name=request.programme_name, pos=pos)

    except Exception as e:
        print(f"Error generating POs: {e}")
        return POResponse(programme_name=request.programme_name, pos=[])

# ── PSO Generator ────────────────────────────────────────────────
def generate_psos(request: PSORequest) -> PSOResponse:
    print(f"\nGenerating {request.n_psos} PSOs for {request.programme_name}")
    try:
        prompt = build_pso_prompt(
            request.programme_name,
            request.course_list,
            request.n_psos
        )
        parsed = call_ollama(prompt)
        psos   = []

        for item in parsed.get("psos", []):
            psos.append(PSOObject(
                pso_id = item.get("pso_id", f"PSO{len(psos)+1}"),
                text   = item.get("text",   ""),
                domain = item.get("domain", "General")
            ))

        print(f"Generated {len(psos)} PSOs")
        save_output(
            {"programme": request.programme_name, "psos": [p.dict() for p in psos]},
            "psos", request.programme_name
        )
        return PSOResponse(programme_name=request.programme_name, psos=psos)

    except Exception as e:
        print(f"Error generating PSOs: {e}")
        return PSOResponse(programme_name=request.programme_name, psos=[])

# ── Combined Generator ───────────────────────────────────────────
def generate_programme(request: ProgrammeRequest) -> ProgrammeResponse:
    print(f"\n{'='*50}")
    print(f"Generating complete programme outcomes for: {request.programme_name}")
    print(f"{'='*50}")

    # Generate all three
    peo_req = PEORequest(
        programme_name=request.programme_name,
        programme_description=request.programme_description,
        n_peos=request.n_peos
    )
    po_req = PORequest(
        programme_name=request.programme_name,
        programme_description=request.programme_description
    )
    pso_req = PSORequest(
        programme_name=request.programme_name,
        course_list=request.course_list,
        n_psos=request.n_psos
    )

    peo_response = generate_peos(peo_req)
    po_response  = generate_pos(po_req)
    pso_response = generate_psos(pso_req)

    print(f"\nComplete programme generated:")
    print(f"  PEOs: {len(peo_response.peos)}")
    print(f"  POs:  {len(po_response.pos)}")
    print(f"  PSOs: {len(pso_response.psos)}")

    # Save combined output
    save_output({
        "programme_name": request.programme_name,
        "generated_at":   datetime.now().isoformat(),
        "peos": [p.dict() for p in peo_response.peos],
        "pos":  [p.dict() for p in po_response.pos],
        "psos": [p.dict() for p in pso_response.psos]
    }, "programme_complete", request.programme_name)

    return ProgrammeResponse(
        programme_name=request.programme_name,
        peos=peo_response.peos,
        pos=po_response.pos,
        psos=pso_response.psos
    )