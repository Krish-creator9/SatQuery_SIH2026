# SIH 2026 PS 26167 — SatQuery AI
## Hardware-Safe Development Plan for Antigravity

**Project constraints:** normal laptops, no dedicated GPU, no paid cloud budget, limited ML knowledge. The system must be CPU-first and must not depend on a large VLM being available locally.

## 1. PS Requirements

**PS ID:** 26167  
**Title:** SatQuery AI - An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries  
**Organization:** ISRO  
**Theme:** Space Technology

Mandatory capabilities:
1. Single-image Visual Question Answering (VQA).
2. One additional single-image task: captioning/scene description OR text-guided region grounding.
3. Bi-temporal change understanding / change-based VQA.
4. Co-registered optical/multispectral + SAR joint analysis.
5. At least one visual/VLM component must be fine-tuned or otherwise adapted using BigEarthNet.txt or open-source training data.
6. Agentic orchestration: query interpretation, input validation, specialist model/tool selection, execution, evidence combination, confidence, and an auditable execution summary.
7. Evidence-grounded textual and visual results.
8. Supported inputs: GeoTIFF/TIFF; PNG/JPEG may be used for prescribed benchmarks.

Datasets explicitly required by the PS:
- BigEarthNet.txt — primary adaptation dataset.
- VRSBench — captioning, grounding and VQA evaluation.
- RSVQA — VQA evaluation.
- CDVQA — bi-temporal/change VQA evaluation.

## 2. Critical Hardware Decision

### Why RS-InternVL3-1B is NOT a hard local dependency

RS-InternVL / InternVL3-1B is attractive because it is remote-sensing-oriented and can be adapted to BigEarthNet. However, it is risky for our current hardware.

Reasons:
- We do not have a dedicated CUDA GPU.
- CPU inference for a multimodal VLM can be too slow for interactive development.
- Practical memory use includes vision encoder, language model, image tensors, cache and framework overhead; quantization helps memory but does not make CPU inference fast.
- Multimodal fine-tuning is substantially harder than inference and is impractical as the main development path without GPU access.
- Making the whole application depend on one heavy VLM creates a single point of failure.
- We have no paid cloud budget.
- The prototype should be reproducible on ordinary student hardware.

**Important:** Do NOT remove the VLM requirement. Keep a lightweight/adaptable VLM module, attempt the smallest feasible adaptation, and keep the rest of the system independent of it. If a GPU becomes temporarily available, use it only for model experiments/fine-tuning. Never claim fine-tuning that was not actually performed.

## 3. Core Architecture

```text
                         USER
                          |
                          v
                  +---------------+
                  | QUERY ANALYZER|
                  +-------+-------+
                          |
                          v
                  +---------------+
                  |EVIDENCE PLANNER|
                  +-------+-------+
                          |
          +---------------+---------------+
          |               |               |
          v               v               v
      OPTICAL           SAR           TEMPORAL
      ANALYSIS        ANALYSIS         ANALYSIS
          |               |               |
          +---------------+---------------+
                          |
                          v
                  +---------------+
                  | EVIDENCE FUSION|
                  +-------+-------+
                          |
              +-----------+-----------+
              |           |           |
              v           v           v
          CONFIDENCE   EXPLANATION  EVIDENCE
                          |
                          v
                    DASHBOARD/REPORT
```

Central principle:

> SatQuery should not just generate an answer. It should determine what evidence is required, run the appropriate analyses, compare the evidence, expose the evidence, and state when evidence is insufficient.

## 4. Simple Meaning of Components

### Query Analyzer
Converts natural language into a task.

Example: “Has the built-up area increased?” -> temporal change analysis, two compatible images, change evidence.

### Evidence Planner
Decides what analysis is needed before answering.

Example:
Question: “What changed between these two images?”
Required: compatibility check, registration, temporal difference, changed-region detection, optional semantic classification.

### Optical Analysis
Works with optical/multispectral imagery:
- NDVI
- NDWI
- spectral statistics
- simple segmentation/classification
- preprocessing

### SAR Analysis
Provides radar-based structural evidence:
- backscatter/texture features
- water/land clues
- temporal SAR change
- complementary evidence when optical imagery is affected by clouds

### Temporal Analysis
Compares images from different dates:
```text
Image A + Image B
        |
registration/alignment
        |
difference/change detection
        |
changed-region map
        |
change statistics
```

### Evidence Fusion
Combines independent evidence.

Example:
- Optical: built-up spectral evidence.
- SAR: structural/backscatter change.
- Temporal: change between dates.

Then produce agreement/disagreement and confidence.

### Evidence-grounded answer
Every important answer should ideally contain:
- answer
- why
- visual evidence
- confidence
- data used
- analyses performed
- warnings

If evidence is insufficient, say so and request the required observation.

## 5. CPU-First Strategy

### Tier 1 — Foundation
Use:
- Python
- NumPy
- OpenCV
- raster/geospatial processing
- scikit-learn where appropriate
- NDVI/NDWI
- image registration
- change detection
- segmentation/classification where practical

These are the core of the working system.

### Tier 2 — Lightweight specialist models
Potential options:
- Grounding DINO base for text-guided boxes.
- SAM or another lightweight segmentation model for visual masks.
- A small VQA/captioning model after hardware testing.

Do not add a model unless it has a clear role and has been tested on remote-sensing imagery.

### Tier 3 — VLM adaptation
The PS requires visual/VLM adaptation.

Process:
1. Start with the smallest feasible open model.
2. Test local inference.
3. Test a tiny adaptation experiment.
4. Measure RAM/VRAM/runtime.
5. Keep it reproducible.
6. If local training is impractical, temporarily use an available GPU machine only for the training experiment, then bring the resulting adapter/checkpoint back.

Do not make cloud hosting a required dependency.

## 6. Model Guidance

### RS-InternVL / InternVL3-1B
Role: potential RS VLM for VQA/captioning/grounding and multimodal analysis.

Status: **OPTIONAL / EXPERIMENTAL, NOT A HARD DEPENDENCY.**

Reason: conceptually strong but risky for CPU-only development and multimodal fine-tuning.

If an RTX 2050 becomes available:
- test inference
- test quantization
- test small adaptation
- measure VRAM
- do not assume it can comfortably fine-tune a multimodal model

### BLIP-2 OPT-2.7B
Avoid as primary:
- larger memory requirement
- not RS-specialized
- no direct grounding output
- poor CPU-first fit

### Grounding DINO Base
Role: text-guided bounding boxes.

Example: “Find water bodies.”

Status: optional specialist tool. Validate on satellite imagery before relying on it.

### SAM / segmentation model
Role: masks for regions and visual evidence.

Status: optional specialist tool, not the main conversational model.

### Qwen-family models
Do not use a text-only Qwen model as if it directly understands satellite images. A text-only model can reason over structured evidence generated by our analysis engine, but it cannot replace a true vision model. If using a multimodal Qwen checkpoint, verify hardware requirements first.

## 7. Main Novelty

Do not pitch the project as “an AI that looks at satellite images.”

Pitch it as:

> **An evidence-driven agentic remote-sensing assistant that dynamically selects the analyses required to answer a natural-language query, combines optical, SAR and temporal evidence, exposes visual evidence and confidence, and identifies when additional observations are required.**

This matches the PS's agentic and evidence-grounded requirements.

## 8. Three Demonstration Modes

Do NOT build three independent AI products. Treat these as application scenarios on the same SatQuery engine.

### A. Disaster Response
Queries:
- “Where are the flood-affected regions?”
- “Show areas where water extent increased.”
- “Compare before and after images.”
- “Which areas require further observation?”

Evidence:
- optical
- SAR
- temporal change
- water indices
- spatial change maps

Avoid claiming certainty about future disasters unless a validated forecasting model exists.

### B. Agriculture Monitoring
Queries:
- “Which regions show vegetation stress?”
- “Where has vegetation decreased?”
- “Show areas with low vegetation health.”
- “Compare crop condition between two dates.”

Evidence:
- NDVI
- temporal change
- optical imagery
- optional SAR

Do not claim exact crop-health diagnosis without validation.

### C. Urban Expansion
Queries:
- “Where has built-up area increased?”
- “Show regions undergoing rapid construction.”
- “Compare urban expansion over two dates.”
- “Which areas require further analysis?”

Evidence:
- temporal change
- optical evidence
- SAR structural evidence
- spatial change map

Do not claim an area is legally suitable for construction. The system provides screening/decision support, not government approval.

## 9. Dashboard

Recommended structure:

```text
+---------------------------------------------------------+
|                    SATQUERY AI                          |
+---------------------------------------------------------+
| Upload Images | Query                                  |
| [Image A] [Image B] [Optical] [SAR]                    |
| Natural Language Query                                  |
| "Has built-up area increased?"                          |
| [ ANALYZE ]                                             |
+---------------------------------------------------------+
| RESULT                                                  |
| Answer: Built-up area increased                         |
| Confidence: 87%                                         |
|                                                         |
| +-------------------+  +----------------------------+   |
| | Change Map        |  | Evidence                    |   |
| | [visual map]      |  | Optical: Supporting         |   |
| |                   |  | SAR: Supporting             |   |
| |                   |  | Temporal: Strong            |   |
| +-------------------+  +----------------------------+   |
| Execution Trace: Query -> Planner -> Analysis -> Fusion|
+---------------------------------------------------------+
```

Any numeric confidence shown in a real demo must be calculated by the implemented system, not hard-coded as a fake result.

## 10. Technology Stack

Frontend:
- React + Vite for a polished dashboard, OR Streamlit for the fastest ML prototype.

Backend:
- Python
- FastAPI

Analysis/ML:
- PyTorch only where required
- Transformers only where required
- OpenCV
- NumPy
- scikit-learn
- rasterio/GDAL-compatible tooling
- GeoPandas where required

Visualization:
- Plotly
- Leaflet / React-Leaflet if an interactive map is needed

Storage:
- local files
- SQLite

No cloud database is necessary for the prototype.

## 11. Development Order

### Phase 1 — Skeleton
Create:
```text
frontend/
backend/
analysis/
models/
data/
outputs/
```
Implement upload API, query API, dashboard and result schema.

### Phase 2 — Image processing
Implement:
- GeoTIFF loading
- metadata extraction
- preview
- compatibility validation
- preprocessing

### Phase 3 — Specialist analysis
Implement:
- NDVI
- NDWI
- image registration
- temporal difference
- change maps
- optical analysis
- SAR feature extraction

### Phase 4 — Evidence Planner
Start rule-based.

Examples:
```text
"compare", "between two dates", "changed" -> TEMPORAL
"water", "flood" -> OPTICAL + WATER
"SAR", "radar" -> SAR
"built-up", "construction" -> OPTICAL + SAR + TEMPORAL
```

Later, add a small language model if useful.

### Phase 5 — Evidence Fusion
Use a standard result structure:
```json
{
  "answer": "...",
  "confidence": 0.87,
  "evidence": [],
  "analyses": [],
  "warnings": [],
  "execution_trace": []
}
```

### Phase 6 — VLM
Only after the above works:
- test lightweight VLM
- test VQA
- test captioning/grounding
- test BigEarthNet adaptation
- integrate only if hardware permits

### Phase 7 — Dashboard polish
Add:
- maps
- overlays
- confidence
- evidence cards
- execution trace
- downloadable report

## 12. Hardware Rules

1. Never assume a GPU exists.
2. Every core feature must have a CPU-compatible path.
3. Never make a large VLM a single point of failure.
4. Do not use paid cloud services as a required dependency.
5. Before downloading any large model, check parameter count, disk size, RAM, VRAM, CPU performance, license and PS relevance.
6. Do not train on the full dataset initially; start with a tiny subset.
7. Never fabricate benchmark scores, confidence, fine-tuning or model results.

## 13. If an RTX 2050 Becomes Available

Use it for:
- small-model inference
- quantized VLM inference
- small LoRA experiments
- segmentation experiments
- benchmarking

First measure:
```text
model load
-> VRAM usage
-> inference latency
-> image resolution
-> batch size
-> stability
```

If it does not fit comfortably, downgrade the model instead of redesigning the project.

## 14. Presentation Positioning

Emphasize:
- **Problem:** remote-sensing users need technical GIS/AI expertise.
- **Solution:** natural-language interaction.
- **Intelligence:** SatQuery determines which evidence is needed.
- **Multimodal reasoning:** optical + SAR + temporal observations.
- **Explainability:** maps, statistics, evidence sources, confidence and execution trace.
- **Safety:** insufficient evidence triggers a request for another observation.
- **Scalability:** specialist modules can later be replaced by stronger models.

## 15. Claims We Must NOT Make

Never claim:
- guaranteed earthquake/flood prediction
- legally verified illegal construction
- exact crop diagnosis without validation
- benchmark accuracy without measuring it
- fine-tuning that was not performed
- universal understanding of all satellite imagery
- certainty from SAR without validation

Use terms such as:
- risk indication
- change detection
- screening
- evidence-based assessment
- decision support
- confidence
- additional observation required

## 16. Final Development Philosophy

```text
             SMALL MODELS
                  +
       CLASSICAL RS ANALYSIS
                  +
           AGENTIC ROUTING
                  +
          EVIDENCE FUSION
                  +
          VISUAL EXPLANATION
                  =
             SATQUERY AI
```

The objective is not to have the biggest model. The objective is to demonstrate a well-designed system that:
1. Understands the query.
2. Determines required evidence.
3. Selects appropriate specialist tools.
4. Processes optical/SAR/temporal data.
5. Combines evidence.
6. Shows evidence visually.
7. Provides confidence.
8. Explains the result.
9. Detects insufficient evidence.
10. Produces an auditable execution trace.

## 17. Instructions to Antigravity

1. Read this file before architecture or model decisions.
2. Treat PS 26167 as the source of truth for mandatory functionality.
3. Keep the project CPU-first.
4. Do not make RS-InternVL3-1B or any large VLM a hard dependency.
5. Do not introduce paid cloud services.
6. Use the PS datasets as the default datasets.
7. Build the specialist remote-sensing pipeline before large AI models.
8. Prefer small, reproducible experiments.
9. Keep every model modular and replaceable.
10. Build the dashboard around evidence, not generated text alone.
11. Preserve an execution trace.
12. Never fabricate benchmark scores or training results.
13. If a proposed model is too heavy, propose a lighter alternative.
14. Ask for confirmation before introducing a large model or paid/cloud dependency.
15. Keep code understandable for a team with limited ML experience.

**Primary principle:**
> Build a robust evidence-driven remote-sensing system first; add VLM intelligence where hardware and validation permit.
