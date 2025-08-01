import uvicorn
import os
from backend.build_frontend import build_vue

def main():
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_file = os.path.join(static_dir, "index.html")

    if not os.path.exists(index_file):
        print("[!] Frontend not found. Building it now...")
        build_vue()

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000)
