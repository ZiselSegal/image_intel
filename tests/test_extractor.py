import pytest
import sys
from pathlib import Path

# 1. מוצאים את הנתיב של התיקייה הנוכחית (tests)
current_dir = Path(__file__).resolve().parent

# 2. מוצאים את הנתיב של תיקיית האב (image_intel) ומוסיפים לה את src
src_path = str(current_dir.parent / "src")

# 3. מוסיפים את הכתובת הזו לרשימת הכתובות של פייתון
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# עכשיו ה-import יעבוד בכל מצב
from extractor import dms_to_decimal, camera_make, has_gps,extract_all,extract_metadata


### 1. בדיקת פונקציית המרת הקואורדינטות (הלוגיקה)
def test_dms_to_decimal_basic():
    # בדיקה פשוטה: 30 מעלות ו-30 דקות צריכות להיות 30.5
    dms = (30, 30, 0)
    ref = 'N'
    assert dms_to_decimal(dms, ref) == 30.5


def test_dms_to_decimal_south_west():
    # בדיקה שדרום (S) או מערב (W) הופכים את המספר לשלילי
    assert dms_to_decimal((10, 0, 0), 'S') == -10.0
    assert dms_to_decimal((20, 0, 0), 'W') == -20.0


def test_dms_to_decimal_invalid_data():
    # בדיקת חסינות: מה קורה כשמקבלים זבל? הפונקציה אמורה להחזיר None ולא לקרוס
    assert dms_to_decimal(None, 'N') is None
    assert dms_to_decimal((30, 30), 'N') is None  # חסר איבר בשלישייה


### 2. בדיקת פונקציות העזר הקטנות
def test_has_gps_logic():
    # בדיקה שהפונקציה מזהה נכון מתי יש ומתי אין GPS במילון
    data_with_gps = {"latitude": 32.1, "longitude": 34.8}
    data_without_gps = {"latitude": None, "longitude": None}

    assert has_gps(data_with_gps) is True
    assert has_gps(data_without_gps) is False


def test_camera_make_cleaning():
    # בדיקה שהפונקציה מנקה תווים ריקים (כמו שתיקנו עם ה-\x00)
    data = {'Make': 'Apple\x00'}
    assert camera_make(data) == 'Apple'

    data_empty = {'Make': '   '}
    assert camera_make(data_empty) == None


### 3. בדיקת "מקרה קצה" ב-extract_metadata
def test_extract_metadata_file_not_found():
    # אנחנו בודקים איך המערכת מגיבה כשמנסים לחלץ מידע מקובץ שלא קיים
    result = extract_metadata("non_existent_image.jpg")

    # המערכת אמורה להחזיר מילון עם ערכי None ולא לקרוס
    assert result["filename"] == "non_existent_image.jpg"
    assert result["has_gps"] is False
    assert result["latitude"] is None


def test_extractor_handles_non_image_files(tmp_path):
    # יצירת קובץ טקסט בתוך תיקיית התמונות
    d = tmp_path / "sub"
    d.mkdir()
    txt_file = d / "not_an_image.txt"
    txt_file.write_text("hello world")

    results = extract_all(str(d))

    # הבדיקה: המערכת לא קרסה והחזירה רשימה ריקה (או דילגה על הקובץ)
    assert len(results) == 0