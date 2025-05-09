import os
import sys
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app

app = create_app()
server = app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True, port=3009)