# KiloLens App

## Basic Installation

```
git clone https://github.com/PurpleMaia/ryan-nupepa-assist
```

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py
```

### Linux or MacOS
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 wsgi.py
```

## Environment Variables

- OPENAI_API_KEY: Set the API key you would like to use.
- KILOLENS_PASSWORD: Set a password for the KiloLens app auth.
- VECTOR_STORE_ID: Set the ID of the vector store you would like to use.

## Usage

1. Adjust port, host, and threads in wsgi.py as needed, then run the script.
2. Open http://localhost:PORT in your browser. Or use from another device with the appropriate IP address. Please note the current build is NOT ready for production use. It is intended for testing purposes only.
3. Log in with the password you set in the environment variables.
4. Use the chat interface to interact with the app.

