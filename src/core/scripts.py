import subprocess
import sys


def run_dev():
    """Run the development server."""
    subprocess.run(["uvicorn", "main:app", "--reload"])

def migrate_generate():
    """Generate a new alembic migration."""
    cmd = ["alembic", "revision", "--autogenerate"]
    # Pass through any additional arguments (like -m "init")
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])
    subprocess.run(cmd)

def migrate_upgrade():
    """Upgrade the database to the latest revision."""
    subprocess.run(["alembic", "upgrade", "head"])

def migrate_downgrade():
    """Downgrade the database by one revision."""
    subprocess.run(["alembic", "downgrade", "-1"])
