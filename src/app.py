from flask import Flask, render_template, request
from map_view import sort_by_time
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_images():

    folder_path = request.form.get('folder_path')

    if not folder_path or not os.path.isdir(folder_path):
        return "תיקייה לא נמצאה", 400

    from extractor import extract_all
    images_data = extract_all(folder_path)

    from map_view import create_map
    map_html = create_map(images_data)

    from timeline import create_timeline
    timeline_html = create_timeline(sort_by_time(images_data))

    from analyzer import analyze
    analysis = analyze(images_data)

    from report import create_report
    report_html = create_report(map_html, timeline_html, analysis)

    return report_html


if __name__ == '__main__':
    app.run(debug=True)