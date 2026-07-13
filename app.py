from flask import Flask, render_template_string, request, jsonify
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)

# Cloudinary কনফিগারেশন
cloudinary.config( 
  cloud_name = "a3hhi2ef",
  api_key = "131227531862894",
  api_secret = "Cv40oj3RRWZPzv8omISqdX6oM3E"
)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Hosting Pro</title>
    <style>
        :root {
            --bg-color: #040712;
            --card-bg: #0b1326;
            --primary: #00f0ff;
            --accent: #bd00ff;
            --success: #00ffcc;
            --text-main: #ffffff;
            --text-muted: #62728b;
            --terminal-bg: #02040a;
        }

        body {
            font-family: 'Segoe UI', Roboto, system-ui, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }

        .container {
            width: 92%;
            max-width: 380px;
            background: linear-gradient(160deg, #0c162b, #040812);
            border-radius: 24px;
            padding: 30px 20px;
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.9), 0 0 40px rgba(0, 240, 255, 0.15);
            text-align: center;
            border: 1px solid rgba(0, 240, 255, 0.15);
            position: relative;
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
        }

        .icon {
            font-size: 45px;
            margin-bottom: 5px;
            display: inline-block;
            animation: float 4s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
        }

        h1 {
            font-size: 26px;
            margin: 0;
            font-weight: 800;
            letter-spacing: 0.5px;
            background: linear-gradient(to right, var(--primary), #b57cff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-muted);
            font-size: 12px;
            margin: 4px 0 25px 0;
        }

        .status-box {
            background: var(--terminal-bg);
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-around;
            font-size: 11px;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-weight: 500;
        }

        .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
        }

        .upload-section {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px 15px;
            margin-bottom: 20px;
            text-align: left;
        }

        .upload-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: block;
        }

        .custom-file-input {
            background: var(--terminal-bg);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 10px;
            padding: 6px;
            display: flex;
            align-items: center;
            position: relative;
            cursor: pointer;
        }

        .custom-file-input.req-input {
            border-color: rgba(208, 0, 255, 0.3);
        }

        .custom-file-input input[type="file"] {
            position: absolute;
            left: 0; top: 0; width: 100%; height: 100%;
            opacity: 0;
            cursor: pointer;
        }

        .file-trigger {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.2), rgba(0, 240, 255, 0.05));
            border: 1px solid rgba(0, 240, 255, 0.5);
            color: var(--primary);
            padding: 8px 14px;
            border-radius: 7px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
        }

        .custom-file-input.req-input .file-trigger {
            background: linear-gradient(135deg, rgba(208, 0, 255, 0.2), rgba(208, 0, 255, 0.05));
            border-color: rgba(208, 0, 255, 0.5);
            color: #bd00ff;
        }

        .file-name-display {
            color: var(--text-muted);
            font-size: 12px;
            margin-left: 12px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-family: monospace;
        }

        .btn-submit {
            background: linear-gradient(135deg, #00b4d8, #5a189a);
            color: white;
            border: none;
            width: 100%;
            padding: 15px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(90, 24, 154, 0.3);
            margin-top: 5px;
        }

        .btn-submit:hover {
            box-shadow: 0 6px 20px rgba(0, 240, 255, 0.4);
            transform: translateY(-1px);
        }

        .history-section {
            margin-top: 25px;
            text-align: left;
        }

        .history-label {
            font-size: 11px;
            color: var(--primary);
            margin-bottom: 6px;
            display: block;
            font-weight: 600;
            text-transform: uppercase;
        }

        .history-list {
            background: var(--terminal-bg);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 12px;
            max-height: 160px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 11px;
        }

        .history-item {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        }

        .history-item:last-child { border-bottom: none; }

        .file-info { color: var(--success); display: block; }
        
        .req-info { color: #cc88ff; display: block; font-size: 10px; margin-top: 2px; }

        .file-link {
            color: var(--primary);
            text-decoration: none;
            word-break: break-all;
            display: inline-block;
            margin-top: 3px;
        }

        .no-history {
            color: var(--text-muted);
            text-align: center;
            font-style: italic;
        }

        .footer {
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 11px;
        }

        .dev-name { color: #cbd5e1; font-weight: 600; }

        .tg-link {
            display: inline-block;
            color: var(--primary);
            text-decoration: none;
            margin-top: 4px;
            font-weight: 600;
        }

        #loading-text {
            display: none;
            color: var(--success);
            font-size: 12px;
            margin-top: 10px;
            font-weight: 600;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <span class="icon">🚀</span>
            <h1>Python Hosting</h1>
            <p class="subtitle">Cloud Console & Multi-File Manager</p>
        </div>

        <div class="status-box">
            <div class="status-item"><span class="dot"></span> Console: Active</div>
            <div class="status-item" style="color: var(--accent);">⚡ Storage: 24/7 Free</div>
        </div>

        <form id="upload-form">
            <div class="upload-section">
                <span class="upload-title" style="color: var(--primary);">1. Upload Script (.py)</span>
                <div class="custom-file-input">
                    <div class="file-trigger">Select Script</div>
                    <div class="file-name-display" id="script-name">No file chosen</div>
                    <input type="file" name="file" id="script-input" required onchange="displayScriptName(this)">
                </div>
                
                <div style="height: 18px;"></div>

                <span class="upload-title" style="color: var(--accent);">2. Upload requirements.txt (Optional)</span>
                <div class="custom-file-input req-input">
                    <div class="file-trigger">Select Reqs</div>
                    <div class="file-name-display" id="req-name">No file chosen</div>
                    <input type="file" name="req_file" id="req-input" onchange="displayReqName(this)">
                </div>
            </div>

            <button type="submit" class="btn-submit">Deploy Project to Cloud</button>
        </form>
        
        <div id="loading-text">⚡ Injecting Core Files into Server...</div>

        <div class="history-section">
            <span class="history-label">📁 Active Live Tunnels (History)</span>
            <div class="history-list" id="history-container">
                <div class="no-history">No active scripts hosted yet.</div>
            </div>
        </div>

        <div class="footer">
            <div class="dev-name">Developer: Abdullah Al Mamun</div>
            <a href="https://t.me/The_Dark_Mamun" target="_blank" class="tg-link">✈ Telegram Channel</a>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", loadHistory);

        function displayScriptName(input) {
            const display = document.getElementById('script-name');
            if(input.files.length > 0) {
                display.innerText = input.files[0].name;
                display.style.color = "var(--success)";
            } else {
                display.innerText = "No file chosen";
                display.style.color = "var(--text-muted)";
            }
        }

        function displayReqName(input) {
            const display = document.getElementById('req-name');
            if(input.files.length > 0) {
                display.innerText = input.files[0].name;
                display.style.color = "var(--success)";
            } else {
                display.innerText = "No file chosen";
                display.style.color = "var(--text-muted)";
            }
        }

        document.getElementById('upload-form').onsubmit = async (e) => {
            e.preventDefault();
            const scriptInput = document.getElementById('script-input');
            const reqInput = document.getElementById('req-input');
            if(scriptInput.files.length === 0) return;

            const scriptName = scriptInput.files[0].name;
            const reqName = reqInput.files.length > 0 ? reqInput.files[0].name : "None";

            const formData = new FormData();
            formData.append("file", scriptInput.files[0]);
            if(reqInput.files.length > 0) {
                formData.append("req_file", reqInput.files[0]);
            }
            
            document.getElementById('loading-text').style.display = 'block';
            
            try {
                const res = await fetch('/upload', { method: 'POST', body: formData });
                const data = await res.json();
                
                if(data.secure_url) {
                    saveToHistory(scriptName, data.secure_url, reqName);
                    document.getElementById('script-name').innerText = "No file chosen";
                    document.getElementById('script-name').style.color = "var(--text-muted)";
                    document.getElementById('req-name').innerText = "No file chosen";
                    document.getElementById('req-name').style.color = "var(--text-muted)";
                    document.getElementById('upload-form').reset();
                } else {
                    alert("Deployment Failed!");
                }
            } catch (err) {
                alert("Server Connection Timeout!");
            } finally {
                document.getElementById('loading-text').style.display = 'none';
            }
        };

        function saveToHistory(name, url, reqName) {
            let history = JSON.parse(localStorage.getItem("hosting_history")) || [];
            history.unshift({ name: name, url: url, reqName: reqName, time: new Date().toLocaleTimeString() });
            localStorage.setItem("hosting_history", JSON.stringify(history));
            loadHistory();
        }

        function loadHistory() {
            let history = JSON.parse(localStorage.getItem("hosting_history")) || [];
            const container = document.getElementById('history-container');
            
            if(history.length === 0) {
                container.innerHTML = '<div class="no-history">No active scripts hosted yet.</div>';
                return;
            }
            
            container.innerHTML = "";
            history.forEach(item => {
                container.innerHTML += `
                    <div class="history-item">
                        <span class="file-info">> [${item.time}] Script: ${item.name}</span>
                        <span class="req-info">⚙ Dependency: ${item.reqName}</span>
                        <a href="${item.url}" target="_blank" class="file-link">${item.url}</a>
                    </div>
                `;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No script file"}), 400
    file_to_upload = request.files['file']
    try:
        upload_result = cloudinary.uploader.upload(file_to_upload, resource_type="auto")
        file_url = upload_result.get('secure_url')
        return jsonify({"secure_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
            font-weight: 500;
        }

        .dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 8px var(--success);
        }

        .upload-section {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 20px 15px;
            margin-bottom: 20px;
            text-align: left;
        }

        .upload-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            display: block;
        }

        /* কাস্টম স্টাইলিশ ফাইল ইনপুট বক্স */
        .custom-file-input {
            background: var(--terminal-bg);
            border: 1px solid rgba(0, 240, 255, 0.2);
            border-radius: 10px;
            padding: 5px;
            display: flex;
            align-items: center;
            position: relative;
            cursor: pointer;
        }

        .custom-file-input.req-input {
            border-color: rgba(208, 0, 255, 0.3);
        }

        /* অরিজিনাল কুৎসিত বাটন লুকানোর ট্রিক */
        .custom-file-input input[type="file"] {
            position: absolute;
            left: 0; top: 0; width: 100%; height: 100%;
            opacity: 0;
            cursor: pointer;
        }

        .file-trigger {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(0, 240, 255, 0.05));
            border: 1px solid rgba(0, 240, 255, 0.4);
            color: var(--primary);
            padding: 8px 14px;
            border-radius: 7px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            white-space: nowrap;
            pointer-events: none;
        }

        .custom-file-input.req-input .file-trigger {
            background: linear-gradient(135deg, rgba(208, 0, 255, 0.15), rgba(208, 0, 255, 0.05));
            border-color: rgba(208, 0, 255, 0.4);
            color: #d000ff;
        }

        .file-name-display {
            color: var(--text-muted);
            font-size: 12px;
            margin-left: 12px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            font-family: monospace;
            pointer-events: none;
        }

        .btn-submit {
            background: linear-gradient(135deg, #00b4d8, #5a189a);
            color: white;
            border: none;
            width: 100%;
            padding: 15px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(90, 24, 154, 0.3);
            margin-top: 5px;
        }

        .btn-submit:hover {
            box-shadow: 0 6px 20px rgba(0, 240, 255, 0.4);
            transform: translateY(-1px);
        }

        .history-section {
            margin-top: 25px;
            text-align: left;
        }

        .history-label {
            font-size: 11px;
            color: var(--primary);
            margin-bottom: 6px;
            display: block;
            font-weight: 600;
            text-transform: uppercase;
        }

        .history-list {
            background: var(--terminal-bg);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 12px;
            max-height: 160px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 11px;
        }

        .history-item {
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        }

        .history-item:last-child { border-bottom: none; }

        .file-info { color: var(--success); display: block; }
        
        .req-info { color: #cc88ff; display: block; font-size: 10px; margin-top: 2px; }

        .file-link {
            color: var(--primary);
            text-decoration: none;
            word-break: break-all;
            display: inline-block;
            margin-top: 3px;
        }

        .no-history {
            color: var(--text-muted);
            text-align: center;
            font-style: italic;
        }

        .footer {
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 11px;
        }

        .dev-name { color: #cbd5e1; font-weight: 600; }

        .tg-link {
            display: inline-block;
            color: var(--primary);
            text-decoration: none;
            margin-top: 4px;
            font-weight: 600;
        }

        #loading-text {
            display: none;
            color: var(--success);
            font-size: 12px;
            margin-top: 10px;
            font-weight: 600;
        }
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <span class="icon">🚀</span>
            <h1>Python Hosting</h1>
            <p class="subtitle">Cloud Console & Multi-File Manager</p>
        </div>

        <div class="status-box">
            <div class="status-item"><span class="dot"></span> Console: Active</div>
            <div class="status-item" style="color: var(--accent);">⚡ Storage: 24/7 Free</div>
        </div>

        <form id="upload-form">
            <div class="upload-section">
                <!-- ১. পাইথন ফাইল কাস্টম বাটন -->
                <span class="upload-title" style="color: var(--primary);">1. Upload Script (.py)</span>
                <div class="custom-file-input">
                    <div class="file-trigger">Select Script</div>
                    <div class="file-name-display" id="script-name">No file chosen</div>
                    <input type="file" name="file" id="script-input" required onchange="displayScriptName(this)">
                </div>
                
                <div style="height: 18px;"></div>

                <!-- ২. requirements.txt কাস্টম বাটন -->
                <span class="upload-title" style="color: var(--accent);">2. Upload requirements.txt (Optional)</span>
                <div class="custom-file-input req-input">
                    <div class="file-trigger">Select Reqs</div>
                    <div class="file-name-display" id="req-name">No file chosen</div>
                    <input type="file" name="req_file" id="req-input" onchange="displayReqName(this)">
                </div>
            </div>

            <button type="submit" class="btn-submit">Deploy Project to Cloud</button>
        </form>
        
        <div id="loading-text">⚡ Injecting Core Files into Server...</div>

        <!-- হিস্ট্রি সেকশন -->
        <div class="history-section">
            <span class="history-label">📁 Active Live Tunnels (History)</span>
            <div class="history-list" id="history-container">
                <div class="no-history">No active scripts hosted yet.</div>
            </div>
        </div>

        <div class="footer">
            <div class="dev-name">Developer: Abdullah Al Mamun</div>
            <a href="https://t.me/The_Dark_Mamun" target="_blank" class="tg-link">✈ Telegram Channel</a>
        </div>
    </div>

    <script>
        document.addEventListener("DOMContentLoaded", loadHistory);

        function displayScriptName(input) {
            const display = document.getElementById('script-name');
            if(input.files.length > 0) {
                display.innerText = input.files[0].name;
                display.style.color = "var(--success)";
            } else {
                display.innerText = "No file chosen";
                display.style.color = "var(--text-muted)";
            }
        }

        function displayReqName(input) {
            const display = document.getElementById('req-name');
            if(input.files.length > 0) {
                display.innerText = input.files[0].name;
                display.style.color = "var(--success)";
            } else {
                display.innerText = "No file chosen";
                display.style.color = "var(--text-muted)";
            }
        }

        document.getElementById('upload-form').onsubmit = async (e) => {
            e.preventDefault();
            const scriptInput = document.getElementById('script-input');
            const reqInput = document.getElementById('req-input');
            if(scriptInput.files.length === 0) return;

            const scriptName = scriptInput.files[0].name;
            const reqName = reqInput.files.length > 0 ? reqInput.files[0].name : "None";

            const formData = new FormData();
            formData.append("file", scriptInput.files[0]);
            if(reqInput.files.length > 0) {
                formData.append("req_file", reqInput.files[0]);
            }
            
            document.getElementById('loading-text').style.display = 'block';
            
            try {
                const res = await fetch('/upload', { method: 'POST', body: formData });
                const data = await res.json();
                
                if(data.secure_url) {
                    saveToHistory(scriptName, data.secure_url, reqName);
                    document.getElementById('script-name').innerText = "No file chosen";
                    document.getElementById('script-name').style.color = "var(--text-muted)";
                    document.getElementById('req-name').innerText = "No file chosen";
                    document.getElementById('req-name').style.color = "var(--text-muted)";
                    document.getElementById('upload-form').reset();
                } else {
                    alert("Deployment Failed!");
                }
            } catch (err) {
                alert("Server Connection Timeout!");
            } finally {
                document.getElementById('loading-text').style.display = 'none';
            }
        };

        function saveToHistory(name, url, reqName) {
            let history = JSON.parse(localStorage.getItem("hosting_history")) || [];
            history.unshift({ name: name, url: url, reqName: reqName, time: new Date().toLocaleTimeString() });
            localStorage.setItem("hosting_history", JSON.stringify(history));
            loadHistory();
        }

        function loadHistory() {
            let history = JSON.parse(localStorage.getItem("hosting_history")) || [];
            const container = document.getElementById('history-container');
            
            if(history.length === 0) {
                container.innerHTML = '<div class="no-history">No active scripts hosted yet.</div>';
                return;
            }
            
            container.innerHTML = "";
            history.forEach(item => {
                container.innerHTML += `
                    <div class="history-item">
                        <span class="file-info">> [${item.time}] Script: ${item.name}</span>
                        <span class="req-info">⚙ Dependency: ${item.reqName}</span>
                        <a href="${item.url}" target="_blank" class="file-link">${item.url}</a>
                    </div>
                `;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No script file"}), 400
    file_to_upload = request.files['file']
    try:
        upload_result = cloudinary.uploader.upload(file_to_upload, resource_type="auto")
        file_url = upload_result.get('secure_url')
        return jsonify({"secure_url": file_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
