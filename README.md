EduAI — Personalized Learning Assistant for SEN Students
========================================================

Requirements
------------
- Python 3.10+ (uses only the standard library: Tkinter + sqlite3)

Run the app
-----------
1) Ensure you are in the project root where `eduai/` lives.  
2) Initialize and start: `python eduai/main.py`  
   - The script ensures the SQLite DB is created/seeded and prints the DB path.

Project layout
--------------
- `eduai/main.py` — entry point; boots the DB then launches the Tkinter window.
- `eduai/db/` — SQLite schema, seed data, and helper functions.
- `eduai/ui/` — UI bootstrap code (currently minimal label).
- `eduai/services/` — service layer placeholders for users, quizzes, and progress.
- `eduai/models/` — domain helpers (difficulty enum, recommender placeholder).
- `eduai/assets/audio_cache/` — cache bucket for generated audio.
- `eduai/data/questions.json` — sample question bank (mirrors seed data).

Notes
-----
- All seed inserts are idempotent; rerunning `main.py` will not duplicate rows.
- Foreign keys are enforced (`PRAGMA foreign_keys=ON`).
