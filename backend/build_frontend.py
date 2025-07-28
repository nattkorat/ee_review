import subprocess
import shutil
import os

def build_vue():
    print("[+] Building frontend...")
    frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")
    static_dir = os.path.join(os.path.dirname(__file__), "..", "backend", "static")

    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        subprocess.run(["npm", "run", "build"], cwd=frontend_dir, check=True)

        # Clear old static
        if os.path.exists(static_dir):
            shutil.rmtree(static_dir)
        os.makedirs(static_dir, exist_ok=True)

        # Copy new build
        dist_dir = os.path.join(frontend_dir, "dist")
        shutil.copytree(dist_dir, static_dir, dirs_exist_ok=True)
        print("[✓] Frontend built successfully.")
    except Exception as e:
        print(f"[!] Error building frontend: {e}")

if __name__ == "__main__":
    build_vue()
    print("[+] Frontend build script executed directly.")
