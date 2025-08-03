let conversation = []

async function sendMessage() {
    const userInput = document.getElementById("userInput");
    const chatBox = document.getElementById("chatBox");
    const message = userInput.value.trim();
    const sendIcon = document.getElementById("sendIcon");
    const waitIcon = document.getElementById("waitIcon");
    const sendButton = document.getElementById("sendButton");

    const temperature = document.getElementById("temperature").value;
    const max_tokens = document.getElementById("maxTokens").value;
    const model = document.getElementById("llmModel").value;
    if (!message) return;

    sendButton.style.cursor = "wait";
    sendButton.style.pointerEvents = "none";
    sendButton.style.background = "var(--color-neutral)";
    sendIcon.style.display = "none";
    waitIcon.style.display = "inline-block";

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
            body: JSON.stringify({messages: conversation, model, temperature, max_tokens})
        });

        const data = await response.json();
        const botReply = data.reply || "No response";

        appendMessage("bot", botReply);
        conversation.push({ role: "assistant", content: botReply });
    } catch (error) {
        appendMessage("bot", "Error reaching server");
    }
    

    sendButton.style.cursor = "pointer";
    sendButton.style.pointerEvents = "auto";
    sendButton.style.background = "var(--color-primary)";
    document.getElementById("sendIcon").style.display = "inline-block";
    document.getElementById("waitIcon").style.display = "none";
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
    appendMessage("bot", "Hi! How can I help you today?");
}

// !! BEGIN CHATGPT GENERATED FUNCTIONS


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

// !! END CHATGPT GENERATED FUNCTIONS

let chatfileinput = null

function addFileToChat() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "*/*";

    input.onchange = async () => {
        chatfileinput = input.files[0];
        alert("File successfully uploaded to chat. Will be included in chat in the next message.");
    }

    input.click();
}

function toggleSettings() {
    const panel = document.getElementById("settingsPanel");
    if (panel.style.display === "none") {
    panel.style.display = "flex";
    } 
    else {
    panel.style.display = "none";
}
}
  
function exportPDF() {
    const doc = new jsPDF();
    doc.save("conversation.pdf");
}

function toggleSidebar() {
        document.getElementById("sidebar").classList.toggle('active');
        document.getElementById("menu-toggle").classList.toggle('active');
    }