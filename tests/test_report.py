import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_path = str(current_dir.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from report import create_report


def test_generate_report_assembly():
    # 1. הכנת נתונים מדומים בפורמט שהפונקציה מצפה לו
    analysis_mock = {
        "date_range": {"start": "01/01/2026", "end": "02/01/2026"},
        "insights": ["נמצאה פעילות חריגה"],
        "unique_cameras": ["Apple iPhone 15", "Canon EOS"],
        "total_images": 10,
        "images_with_gps": 8
    }

    map_html_mock = "<div>MAP</div>"
    timeline_html_mock = "<div>TIMELINE</div>"

    # 2. קריאה לפונקציה עם הסדר הנכון של הפרמטרים
    full_report = create_report(map_html_mock, timeline_html_mock, analysis_mock)

    # 3. בדיקות
    assert "MAP" in full_report
    assert "TIMELINE" in full_report
    assert "iPhone 15" in full_report