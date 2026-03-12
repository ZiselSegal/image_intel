import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_path = str(current_dir.parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from analyzer import get_total_images, get_unique_cameras, get_device_changes,analyze


def test_analyzer_statistics():
    # נתונים מדומים לבדיקה
    fake_data = [
        {'camera_make': 'Apple', 'camera_model': 'iPhone 15'},
        {'camera_make': 'Apple', 'camera_model': 'iPhone 15'},
        {'camera_make': 'Samsung', 'camera_model': 'S23'}
    ]

    # בדיקת ספירת תמונות
    assert get_total_images(fake_data) == 3

    # בדיקת זיהוי מכשירים ייחודיים (צריך להיות 2)
    unique_cameras = get_unique_cameras(fake_data)
    assert len(unique_cameras) == 2
    assert "Apple iPhone 15" in unique_cameras


def test_device_change_detection():
    # בדיקה שהמערכת מזהה מעבר בין יצרנים שונים
    data = [
        {'camera_make': 'Apple', 'camera_model': 'iPhone 15', 'datetime': '2025:01:01 10:00:00'},
        {'camera_make': 'Samsung', 'camera_model': 'S23', 'datetime': '2025:01:01 11:00:00'}
    ]

    changes = get_device_changes(data)
    # אמורה להיות הודעה על החלפת מכשיר
    assert any("החלפת מכשיר" in change for change in changes)


def test_no_device_changes():
    # בדיקה שלא מדווחת החלפה כשזה אותו מכשיר
    data = [
        {'camera_make': 'Apple', 'camera_model': 'iPhone 15'},
        {'camera_make': 'Apple', 'camera_model': 'iPhone 15'}
    ]
    changes = get_device_changes(data)
    assert "לא נמצאו החלפות מכשירים" in changes[0]


def test_analyze_with_single_image():
    single_data = [{
        'datetime': '2026:01:01 10:00:00',
        'camera_make': 'Apple',
        'camera_model': 'iPhone',
        'latitude': 32.0,
        'longitude': 34.0
    }]
    res = analyze(single_data)

    # בודקים שהטווח לא קורס ומציג את אותו תאריך
    assert res['date_range']['start'] == '2026:01:01 10:00:00'
    assert res['total_images'] == 1