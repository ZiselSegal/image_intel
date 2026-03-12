import sys
from pathlib import Path

# הגדרת נתיבים ל-src
current_dir = Path(__file__).resolve().parent
src_path = str(current_dir.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from extractor import extract_all
from map_view import create_map, sort_by_time
from timeline import create_timeline
from analyzer import analyze  # ייבוא הפונקציה המרכזית מהאנלייזר
from report import create_report # ייבוא פונקציית הדו"ח

def test_full_app_flow():
    """בדיקה שמדמה את הזרימה המלאה של האפליקציה בדומה ל-app.py"""

    # 1. נתיב לתיקיית תמונות (או תיקייה זמנית)
    test_images_path = "images"

    # 2. שלב החילוץ (Extractor)
    images_data = extract_all(test_images_path)
    assert isinstance(images_data, list)

    if len(images_data) > 0:
        # 3. שלב המיון (Map View / Utils)
        sorted_data = sort_by_time(images_data)

        # 4. שלב הניתוח המלא (Analyzer) - בודקים שזה מייצר את מילון ה-analysis
        analysis = analyze(sorted_data)
        assert isinstance(analysis, dict)
        assert "date_range" in analysis # וידוא שהמפתחות שהדו"ח צריך קיימים

        # 5. שלב יצירת רכיבי הויזואליזציה
        map_html = create_map(sorted_data)
        timeline_html = create_timeline(sorted_data)

        # 6. השלב הסופי - יצירת הדו"ח המאוחד (Report)
        # זה השלב שמוודא שכל הפרמטרים מתחברים נכון
        final_report = create_report(map_html, timeline_html, analysis)

        # בדיקות איכות לתוצאה הסופית
        assert "<html>" in final_report.lower()
        assert "Image Intel" in final_report
        assert "סיכום פעילות" in final_report
        assert "timeline-wrapper" in final_report
    else:
        # טיפול בתיקייה ריקה
        assert len(images_data) == 0