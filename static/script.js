function addMessage(sender, text) {
    const chat = document.getElementById("chat");
    chat.innerHTML += `<p><b>${sender}:</b> ${text}</p>`;
    chat.scrollTop = chat.scrollHeight;
}

function sendText() {
    const input = document.getElementById("input").value;
    addMessage("You", input);

    fetch("/api/process/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ command: input })
    })
    .then(res => res.json())
    .then(data => {
        addMessage("Jarvis", data.response);

        if (data.steps) {
            addMessage("Steps", data.steps);
        }

        if (data.graph) {
            document.getElementById("graph").innerHTML = `<img src="${data.graph}">`;
        }

        speak(data.response);
        performAction(data.action, data.query);
    });
}

function performAction(action, query) {
    if (!action) return;

    if (action === "youtube_play") {
        window.open(`https://www.youtube.com/results?search_query=${query}`);
    }

    if (action === "spotify") {
        window.open("https://open.spotify.com");
    }

    if (action === "news") {
        window.open("https://news.google.com");
    }

    if (action === "search") {
        window.open(`https://www.google.com/search?q=${query}`);
    }
}

function startListening() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.onresult = function(e) {
        const text = e.results[0][0].transcript;
        document.getElementById("input").value = text;
        sendText();
    };

    recognition.start();
}

function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}
