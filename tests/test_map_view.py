import sys
import os
from pathlib import Path

# הגדרת נתיב דינמית כדי שפייתון ימצא את תיקיית src
current_dir = Path(__file__).resolve().parent
src_path = str(current_dir.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# ייבוא הפונקציות מתוך map_view.py
from map_view import create_map, sort_by_time


# --- בדיקות עבור פונקציית המיון (sort_by_time) ---

def test_sort_by_time_correct_order():
    """בדיקה שהפונקציה ממיינת תמונות מהמוקדם למאוחר"""
    unordered_data = [
        {'filename': 'late.jpg', 'datetime': '2025:01:01 15:00:00'},
        {'filename': 'early.jpg', 'datetime': '2025:01:01 08:00:00'},
        {'filename': 'middle.jpg', 'datetime': '2025:01:01 12:00:00'}
    ]

    sorted_data = sort_by_time(unordered_data)

    assert sorted_data[0]['filename'] == 'early.jpg'
    assert sorted_data[1]['filename'] == 'middle.jpg'
    assert sorted_data[2]['filename'] == 'late.jpg'


def test_sort_by_time_with_missing_dates():
    """בדיקה שהפונקציה לא קורסת אם לאחת התמונות אין תאריך"""
    data = [
        {'filename': 'with_date.jpg', 'datetime': '2025:01:01 10:00:00'},
        {'filename': 'no_date.jpg', 'datetime': None}
    ]
    # לא אמורה להיזרק שגיאה
    result = sort_by_time(data)
    assert len(result) == 2


# --- בדיקות עבור יצירת המפה (create_map) ---

def test_create_map_html_structure():
    """בדיקה שהמפה מחזירה מחרוזת HTML תקינה המכילה את נתוני התמונות"""
    test_data = [
        {
            'has_gps': True,
            'latitude': 32.0,
            'longitude': 34.0,
            'camera_make': 'Apple',
            'filename': 'test_image.jpg',
            'full_path': 'C:/images/test_image.jpg'
        }
    ]

    html = create_map(test_data)

    assert isinstance(html, str)
    assert 'test_image.jpg' in html
    # בדיקה שהצבע של Apple (אדום) נכנס לקוד המפה
    assert 'red' in html


def test_create_map_no_gps_data():
    """בדיקה שהמערכת מציגה הודעת שגיאה מעוצבת כשאין נתוני מיקום"""
    test_data = [{'has_gps': False, 'filename': 'no_gps.jpg'}]

    html = create_map(test_data)

    assert "No GPS Data Found" in html
    assert "האנלייזר לא מצא מידע גאוגרפי" in html


def test_polyline_in_map():
    """בדיקה שהקו הסגול (PolyLine) מתווסף למפה כשיש מסלול"""
    test_data = [
        {'has_gps': True, 'latitude': 32.0, 'longitude': 34.0, 'datetime': '2025:01:01 10:00:00'},
        {'has_gps': True, 'latitude': 32.1, 'longitude': 34.1, 'datetime': '2025:01:01 11:00:00'}
    ]

    html = create_map(test_data)

    # בדיקה שקוד המפה מכיל התייחסות לצבע הסגול של המסלול
    assert 'purple' in html