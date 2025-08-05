from app import app
from waitress import serve

# Run the app with this script. Adjust the host, port, and threads parameters as needed.
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=54311, threads=32)