"""Train Orchestration."""
from aihero.research.orchestration.train import delete, launch
from dotenv import load_dotenv
from fire import Fire

load_dotenv()
if __name__ == "__main__":
    Fire(
        {
            "launch": launch,
            "delete": delete,
        }
    )
