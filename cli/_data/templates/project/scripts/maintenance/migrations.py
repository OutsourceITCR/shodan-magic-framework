import subprocess
from config import services

for service in services:
    print(f"Running migrations for {service}...")
    subprocess.run(["alembic", "upgrade", "head"], cwd=f"./{service}/")