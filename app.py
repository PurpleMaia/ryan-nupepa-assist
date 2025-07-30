from flask import Flask, render_template, request, jsonify, flash, redirect
from openai import OpenAI
import os

# Initialize Flask App
app = Flask(__name__)

# Initialize OpenAI Client. Store your key in an environment variable called OPENAI_API_KEY
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Render the homepage (url/)
@app.route("/")
def home():
    return render_template("index.html")

# Render the actual app (url/app)
@app.route("/app")
def about():
    return render_template("chat.html")

@app.route("/under-construction")
def under_construction():
    return render_template("under-construction.html")

# OpenAI API call handling. Send a POST request to /chat with a JSON payload containing the user"s message.
@app.route("/chat", methods=["POST"])
def chat():
    messages = request.json.get("messages", []) 
    model = request.json.get("model", "gpt-4.1-mini")
    temperature = float(request.json.get("temperature", 0.7))
    max_tokens = int(request.json.get("max_tokens", 4096))

    response_parameters = {
        "model": model,
        "max_output_tokens": max_tokens,
        "tools": [{
            "type": "file_search",
            "vector_store_ids": ["vs_6875a8264e04819181f92591e60c1054"],
            "max_num_results": 20
        }],
        "input": messages,
        "instructions": "You are KumuComputer, a helpful assistant that helps the user to research parts of Hawaiian History. Utilize relevant files to craft a response that satisfies the user's request. IMPORTANT: Be sure to ALWAYS cite the file you pull information from at then end of your message."
    }

    # Temperature is not supported for these models and must be omitted.
    no_temperature_models = {"o3", "o3-pro", "o4-mini"}
    if model not in no_temperature_models:
        response_parameters["temperature"] = temperature

    response = client.responses.create(**response_parameters)

    reply = response.output_text
    print(response)
    return jsonify({"reply": reply})

# Handle file uploads. Send a POST request to /upload with a JSON payload containing the file.
# The file will first be uploaded to your OpenAI account, then assigned to the vector store.
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    
    fileupload = client.files.create(
        file=(file.filename, file.stream),
        purpose="assistants"
    )

    client.vector_stores.files.create(
        vector_store_id="vs_6875a8264e04819181f92591e60c1054",
        file_id=fileupload.id
    )

    return jsonify({"message": f"Uploaded: {file.filename}"})

# @app.route("/getfiles", methods=["GET"])
# def get_files():
#     files = client.vector_stores.files.list(vector_store_id="vs_6875a8264e04819181f92591e60c1054")
#     return jsonify({"filelist": files})

# When running the app with this script. Do not use this for production.
if __name__ == "__main__":
    app.run(debug=True)
