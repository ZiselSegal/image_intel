import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_path = str(current_dir.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from timeline import create_timeline


def test_timeline_structure_always_exists():
    """בדיקה שהמבנה הבסיסי וה-CSS תמיד נוצרים, גם כשאין תמונות"""
    html_output = create_timeline([])

    # בודק שה-CSS והקונטיינר קיימים
    assert 'class="timeline-wrapper"' in html_output
    assert 'border-right: 3px solid #00d2ff;' in html_output
    # וודא שהלולאה לא ייצרה כרטיסים כשאין נתונים
    assert 'class="event-card"' not in html_output


def test_timeline_with_and_without_location():
    """בדיקה שהטיימליין מייצר כפתור מפה רק כשיש קואורדינטות"""
    test_data = [
        {
            'datetime': '2026:01:01 10:00:00',
            'camera_make': 'Apple',
            'camera_model': 'iPhone 15',
            'latitude': 32.0853,
            'longitude': 34.7818
        },
        {
            'datetime': '2026:01:01 12:00:00',
            'camera_make': 'Samsung',
            'camera_model': 'S24',
            'latitude': None,  # אין מיקום
            'longitude': None
        }
    ]

    html_output = create_timeline(test_data)

    # בדיקת הכרטיס עם המיקום[cite: 1]
    assert 'Open Map' in html_output
    assert 'https://www.google.com/maps?q=32.0853,34.7818' in html_output

    # בדיקת הכרטיס בלי המיקום (צריך להופיע אבל בלי הכפתור)[cite: 1]
    assert 'Samsung S24' in html_output
    # מוודא שהכפתור לא מופיע פעמיים (הוא אמור להופיע רק פעם אחת עבור התמונה הראשונה)
    assert html_output.count('class="map-btn"') == 1


def test_timeline_skips_no_date():
    """בדיקה שתמונות ללא תאריך לא מייצרות כרטיס בכלל"""
    test_data = [{'datetime': None, 'camera_make': 'Nokia'}]
    html_output = create_timeline(test_data)

    assert 'Nokia' not in html_output