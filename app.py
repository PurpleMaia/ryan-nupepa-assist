from flask import Flask, render_template, request, jsonify, Response
from openai import OpenAI
import os

# Initialize Flask App
app = Flask(__name__)

# Initialize OpenAI Client. Store your key in an environment variable called OPENAI_API_KEY
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
VECTOR_STORE_ID = os.environ.get("VECTOR_STORE_ID")
PASSWORD = os.environ.get("KILOLENS_PASSWORD")
USERNAME = "demo" # ! Set the username here.

client = OpenAI(api_key=OPENAI_API_KEY)

# This function reads the auth header and checks if the username and password match the expected values.
# If the username and password match, it returns True. Otherwise, it returns False.
def check_auth(auth):
    return auth and auth.username == USERNAME and auth.password == PASSWORD

# If credentials are not provided, this function will prompt the user to enter them.
# In most browsers, this will prompt the user to enter their credentials via a pop-up window.
def authenticate():
    return Response(
        'Please log in to use KiloLens', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Render the homepage (url/)
@app.route("/")
def home():
    return render_template("index.html")

# ! PROTECTED ROUTE
# Render the actual app (url/app)
@app.route("/app")
def app():

    auth = request.authorization
    if not check_auth(auth):
        return authenticate()
    
    return render_template("chat.html")

# ! PROTECTED ROUTE
# OpenAI API call handling. Send a POST request to /chat with a JSON payload containing the user"s message.
@app.route("/chat", methods=["POST"])
def chat():
    
    auth = request.authorization
    if not check_auth(auth):
        return authenticate()
    
    # Retrieve relevant information from the JSON payload.
    messages = request.json.get("messages", []) 
    model = request.json.get("model", "gpt-4.1-mini")
    temperature = float(request.json.get("temperature", 0.7))
    max_tokens = int(request.json.get("max_tokens", 4096))

    # Read the prompt from a file. Alternatively you can hardcode the prompt here.
    prompt = open("./prompt.txt", "r").read()

    # Start building the response parameters to be sent. Differs based on model and inputs.
    response_parameters = {
        "model": model,
        "max_output_tokens": max_tokens,
        "tools": [{
            "type": "file_search",
            "vector_store_ids": ["vs_6875a8264e04819181f92591e60c1054"],
            "max_num_results": 20
        }],
        "input": messages,
        "instructions": prompt
    }

    # Temperature is not supported for these models and must be omitted.
    # Add the temperature parameter if the model is not in this list.
    no_temperature_models = {"o3", "o3-pro", "o4-mini"}
    if model not in no_temperature_models:
        response_parameters["temperature"] = temperature

    # If the user has uploaded a file, add it to the response parameters
    # TODO: Implement direct file/audio uploads. Currently, only vector store files are supported.
    # TODO: Use Whisper to process the audio files and simply add any files to the response parameters.

    # Create the response using the parameters.
    response = client.responses.create(**response_parameters)

    # Extract the latest reply from the response.
    reply = response.output_text

    # Return the reply as a JSON response.
    return jsonify({"reply": reply})

# ! PROTECTED ROUTE
# Handle file uploads. Send a POST request to /upload with a JSON payload containing the file.
# The file will first be uploaded to your OpenAI account, then assigned to the vector store.
@app.route("/upload", methods=["POST"])
def upload_file():

    auth = request.authorization
    if not check_auth(auth):
        return authenticate()
    
    # Check if the file is included in the request. If not, return an error. Bad request.
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    # Get the file from the request.
    file = request.files["file"]

    # Check if the file has a filename. If not, return an error. Bad request.
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    
    # First, upload the file to OpenAI. This will return a file object containing the file ID.
    fileupload = client.files.create(
        file=(file.filename, file.stream),
        purpose="assistants"
    )

    # Then, assign the file to the vector store using the file ID obtained from the upload.
    client.vector_stores.files.create(
        vector_store_id="vs_6875a8264e04819181f92591e60c1054",
        file_id=fileupload.id
    )

    # Log the file upload to a file. This is just for debugging purposes to keep track of which files have been uploaded.
    with open("./fileuploadlog.txt", "a") as f:
        f.write(f"{file.filename} || {fileupload.id}\n")

    # Return a success message.
    return jsonify({"message": f"Uploaded: {file.filename}. It may take a few minutes for the file to be processed."})

# When running the app with this script. Do not use this for production.
# This mode is good for development and testing, such as when you are working on the app.
if __name__ == "__main__":
    app.run(debug=True)
