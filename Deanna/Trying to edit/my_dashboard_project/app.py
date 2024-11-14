from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Route for the main dashboard page
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route to serve the individual HTML files (tab content)
@app.route('/html_files/<filename>')
def serve_html_file(filename):
    try:
        return send_from_directory('html_files', filename)
    except FileNotFoundError:
        return f"File{filename} not found", 404

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/test')
def test_file():
    return send_from_directory('html_files', 'file1.html')