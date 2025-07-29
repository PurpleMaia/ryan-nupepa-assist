let conversation = []

async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to UI and conversation array
    appendMessage("user", message);
    conversation.push({ role: "user", content: message });
    userInput.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ messages: conversation })
        });

        const data = await response.json();
        const botReply = data.reply || "No response";

        appendMessage("bot", botReply);
        conversation.push({ role: "assistant", content: botReply });
    } catch (error) {
        appendMessage("bot", "Error reaching server");
    }
}


function appendMessage(sender, text) {
    const chatBox = document.getElementById("chatBox");

    const messageElem = document.createElement("div");
    messageElem.className = `chat-message ${sender}`;

    messageElem.innerHTML = DOMPurify.sanitize(marked.parse(text));

    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function clearChat() {
    document.getElementById("chatBox").innerHTML = "";
}


function addFile() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "*/*";

    input.onchange = async () => {
        const file = input.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();
            alert(result.message);
        } catch (err) {
            alert("File upload failed.");
            console.error(err);
        }
    };

    input.click();
}

// !! BEGIN CHATGPT GENERATED FUNCTIONS
function toggleSettings() {
    const panel = document.getElementById("settingsPanel");
    panel.style.display = panel.style.display === "none" ? "block" : "none";
  }

  document.getElementById("temperature")?.addEventListener("input", function () {
    document.getElementById("tempValue").innerText = this.value;
});
// !! END CHATGPT GENERATED FUNCTIONS