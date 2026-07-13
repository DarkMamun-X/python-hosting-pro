from flask import Flask, render_template_string, request
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
    <title>Python Hosting & Cloud Storage</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #0f172a; color: #f8fafc; text-align: center; padding: 20px; }
        .container { background: #1e293b; padding: 25px; border-radius: 16px; display: inline-block; width: 90%; max-width: 330px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        h1 { color: #38bdf8; font-size: 22px; margin-bottom: 5px; }
        p { color: #94a3b8; font-size: 13px; }
        input[type="file"] { margin: 20px 0; color: #cbd5e1; font-size: 13px; }
        button { background: #2563eb; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; font-size: 14px; }
        button:hover { background: #1d4ed8; }
        .result { margin-top: 20px; word-break: break-all; font-size: 13px; color: #4ade80; background: #0f172a; padding: 12px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Python Hosting</h1>
        <p>24/7 Server & Cloud Storage Active</p>
        
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <button type="submit">Upload to Cloud</button>
        </form>

        {% if file_url %}
        <div class="result">
            <p style="margin: 0 0 5px 0;"><strong>Upload Successful!</strong></p>
            <a href="{{ file_url }}" target="_blank" style="color:#38bdf8; text-decoration: none;">Click Here to Open File</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file selected", 400
    
    file_to_upload = request.files['file']
    if file_to_upload:
        # ক্লাউডিনারিতে ফাইল আপলোড হচ্ছে
        upload_result = cloudinary.uploader.upload(file_to_upload, resource_type="auto")
        file_url = upload_result.get('secure_url')
        return render_template_string(HTML_TEMPLATE, file_url=file_url)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
