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

def test_app_to_report_connection(client, tmp_path):
    """
    בדיקה שה-app באמת משתמש ב-report.py כדי לייצר את התשובה הסופית
    """
    # 1. יצירת תיקייה עם תמונה דמי (או תיקייה ריקה)
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()

    # 2. שליחת בקשה לשרת
    response = client.post('/analyze', data={'folder_path': str(test_dir)})

    # 3. פענוח התשובה
    html_res = response.data.decode('utf-8')

    # 4. הבדיקה הקריטית: האם מופיעים אלמנטים שקיימים *רק* ב-report.py?
    # אלו מוודאים שה-app באמת קרא ל-create_report והשתמש בתוצאה שלו
    assert "Image Intel | דוח מודיעין חזותי" in html_res  # כותרת ה-H1 מהדו"ח
    assert "טווח פעילות:" in html_res  # טקסט ייחודי מהדו"ח
    assert "toggleTimeline()" in html_res  # הסקריפט שנמצא בדו"ח
    assert "stat-card" in html_res  # מחלקת ה-CSS מהדו"ח