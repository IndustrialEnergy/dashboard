import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Unset DATA_DIR if it's set to the Docker path when running locally
if os.getenv("DATA_DIR") == "/app/data/final":
    del os.environ["DATA_DIR"]

from app import create_app

app = create_app()
server = app.server

if __name__ == "__main__":
    # Get debug mode from environment variable in .env, default to True
    debug_mode = os.getenv("DASH_DEBUG", "true").lower() == "true"
    app.run_server(host="0.0.0.0", debug=debug_mode, port=3009)
