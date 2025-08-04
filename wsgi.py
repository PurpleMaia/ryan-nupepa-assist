from app import app
from waitress import serve
import os

PORT = os.getenv("PORT",54311)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=PORT)