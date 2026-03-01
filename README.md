EduAI — Personalized Learning Assistant for SEN Students

## Overview
EduAI is a desktop learning assistant focused on supporting students with special educational needs (SEN).
Current quiz subjects:
- Math
- English

In the dashboard you can:
- choose quiz subject (`Math` or `English`) before starting a session
- filter Overview/Sessions/Recommendations by subject (`All/Math/English`)

## Prerequisites
- Python 3.10+ 
- `pip` available on PATH

## Installation
1. Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
```
```bash
# macOS / Linux
source .venv/bin/activate
```
```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

If you see an error like "gTTS is not installed", install it directly:
```bash
pip install gTTS
```

## Run
```bash
python3 main.py
```

