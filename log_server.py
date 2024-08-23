from flask import Flask, render_template_string, send_from_directory, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the path to the log folder
LOG_FOLDER = 'logs'
app.config['LOG_FOLDER'] = LOG_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# HTML template to list files, show file content, and upload new files
list_template = '''
<!doctype html>
<html>
<head><title>Log Files</title></head>
<body>
<h1>Log Files</h1>
<ul>
{% for file in files %}
  <li><a href="/logs/{{ file }}">{{ file }}</a></li>
{% endfor %}
</ul>
</body>
</html>
'''

file_template = '''
<!doctype html>
<html>
<head><title>{{ filename }}</title></head>
<body>
<h1>Content of {{ filename }}</h1>
<a href="/">Back to file list</a>
<pre>{{ content }}</pre>
</body>
</html>
'''

@app.route('/')
def list_logs():
    # Get list of files in the log folder
    files = os.listdir(LOG_FOLDER)
    return render_template_string(list_template, files=files)

@app.route('/logs/<path:filename>')
def show_log(filename):
    # Ensure the file path is secure
    filepath = os.path.join(LOG_FOLDER, filename)
    if not os.path.isfile(filepath):
        return "File not found", 404

    with open(filepath, 'r') as file:
        content = file.read()
    return render_template_string(file_template, filename=filename, content=content)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('list_logs'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('list_logs'))

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['LOG_FOLDER'], filename))
        return redirect(url_for('list_logs'))

if __name__ == '__main__':
    # Ensure log directory exists
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    app.run(debug=True)
