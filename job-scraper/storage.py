import json
from pathlib import Path

seen_file = Path("seen_jobs.json")

def load_seen_jobs() -> set:
    if not seen_file.exists():
        return set()
    return set(json.loads(seen_file.read_text()))


def save_seen_jobs(seen:set):
    seen_file.write_text(json.dumps(list(seen)))


def filter_new_jobs(jobs:list[dict]) -> list[dict]:
    seen = load_seen_jobs()
    new_jobs = [job for job in jobs if job["id"] not in seen]
    seen.update(job["id"] for job in new_jobs)
    save_seen_jobs(seen)
    return new_jobs


    