import sys
from pathlib import Path
import pytest

# הגדרת נתיבים
current_dir = Path(__file__).resolve().parent
src_path = str(current_dir.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from app import app


@pytest.fixture
def client():
    """יוצר לקוח בדיקה עבור Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """בדיקה שדף הבית נטען בהצלחה"""
    response = client.get('/')
    assert response.status_code == 200


def test_analyze_invalid_path(client):
    """בדיקה ששליחת נתיב לא קיים מחזירה שגיאה 400"""
    response = client.post('/analyze', data={'folder_path': '/non/existent/path'})
    assert response.status_code == 400

    # הופכים את הבייטים לטקסט רגיל ובודקים את התוכן
    error_message = response.data.decode('utf-8')
    assert "תיקייה לא נמצאה" in error_message


def test_full_analysis_flow(client, tmp_path):
    """בדיקה שהזרמת הנתונים המלאה בשרת עובדת (מקצה לקצה)"""
    # יצירת תיקייה זמנית ריקה כדי שלא נקבל 400
    test_folder = tmp_path / "empty_images"
    test_folder.mkdir()

    # שליחת בקשת POST לשרת עם הנתיב הזמני
    response = client.post('/analyze', data={'folder_path': str(test_folder)})

    # בדיקה שהשרת החזיר דף HTML (סטטוס 200)
    assert response.status_code == 200
    # בדיקה שה-HTML מכיל אלמנטים מהדו"ח
    html_content = response.data.decode('utf-8')
    assert "Image Intel" in html_content
    assert "ציר זמן" in html_content

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