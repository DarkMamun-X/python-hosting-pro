from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Hosting</title>
    <style>
        body { font-family: sans-serif; background-color: #0f172a; color: #f8fafc; text-align: center; padding-top: 50px; }
        .container { background: #1e293b; padding: 30px; border-radius: 16px; display: inline-block; width: 300px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; margin-bottom: 5px; }
        .status { color: #4ade80; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Python Hosting</h1>
        <p style="color:#94a3b8; margin-top:0;">24/7 Cloud Environment</p>
        <p>Status: <span class="status">● ONLINE (24/7)</span></p>
        <p>Storage: Active & Unlimited</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    # Render-এর নিজস্ব পোর্টের জন্য os.environ.get ব্যবহার করা হয়েছে
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
  
