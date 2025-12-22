from pathlib import Path

from db.database import ensure_db_ready, DB_PATH
from ui.app import launch_app


def main() -> None:
    ensure_db_ready()
    print(f"DB ready at {Path(DB_PATH).resolve()}")
    launch_app()


if __name__ == "__main__":
    main()
