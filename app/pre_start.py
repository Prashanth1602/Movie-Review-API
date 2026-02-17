from tenacity import retry, stop_after_attempt, wait_fixed
from app.core.database import SessionLocal
from sqlalchemy import text

max_tries = 60 * 5
wait_seconds = 1

@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
)
def init() -> None:
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
    except Exception as e:
        raise e

def main() -> None:
    init()

if __name__ == "__main__":
    main()
