<?php
$backend = "http://localhost:5000";
?>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>G4F AI Studio - PHP</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .chat-box { height: 60vh; overflow-y: auto; background: #f8f9fa; padding: 15px; border-radius: 10px; }
        .message { padding: 10px 15px; border-radius: 18px; margin-bottom: 10px; max-width: 80%; }
        .user { background: #0d6efd; color: white; margin-left: auto; }
        .assistant { background: #e9ecef; }
    </style>
</head>
<body class="bg-light">
<div class="container py-4">
    <div class="card shadow">
        <div class="card-header bg-primary text-white">
            <h4 class="mb-0">G4F AI Studio (PHP Version)</h4>
        </div>
        <div class="card-body">
            <div class="chat-box mb-3" id="chatBox"></div>
            <div class="input-group">
                <input type="text" id="chatInput" class="form-control" placeholder="Ketik pesan..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button class="btn btn-primary" onclick="sendMessage()">Kirim</button>
            </div>
        </div>
    </div>
</div>

<script>
const BACKEND = '<?php echo $backend; ?>';

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const chatBox = document.getElementById('chatBox');
    const msg = input.value.trim();
    if (!msg) return;

    chatBox.innerHTML += `<div class="message user"><strong>Kamu:</strong> ${msg}</div>`;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.innerHTML = '<strong>AI:</strong> <span class="spinner-border spinner-border-sm"></span> Mengetik...';
    chatBox.appendChild(loadingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const res = await fetch(`${BACKEND}/chat`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                model: 'gpt-4o-mini',
                messages: [{role: 'user', content: msg}],
                stream: false
            })
        });

        const data = await res.json();
        loadingDiv.remove();

        if (data.choices && data.choices[0]) {
            const reply = data.choices[0].message.content;
            chatBox.innerHTML += `<div class="message assistant"><strong>AI:</strong> ${reply}</div>`;
        } else {
            chatBox.innerHTML += `<div class="message assistant text-danger">Error: ${data.error || 'Unknown error'}</div>`;
        }
    } catch (e) {
        loadingDiv.remove();
        chatBox.innerHTML += `<div class="message assistant text-danger">Connection error</div>`;
    }
    chatBox.scrollTop = chatBox.scrollHeight;
}
</script>
</body>
</html>