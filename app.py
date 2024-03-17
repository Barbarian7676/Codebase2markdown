from flask import Flask, request, send_file, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string(open("index.html").read())

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('file')  # Get files
    extension_filter = request.form.get('extension_filter', '.py').split(',')  # Get extensions
    output_file_name = request.form.get('output_file_name', 'output_markdown.md')  # Get output file name

    with open(output_file_name, 'w', encoding='utf-8') as markdown_file:
        for file in files:
            filename = secure_filename(file.filename)
            if any(filename.endswith(ext) for ext in extension_filter):  # Filter files by extension
                file_contents = file.read().decode('utf-8')
                markdown_file.write(f"\n# {filename}\n```python\n{file_contents}\n```\n")
    
    return send_file(output_file_name, as_attachment=True, download_name=output_file_name)

if __name__ == '__main__':
    app.run(debug=True)
