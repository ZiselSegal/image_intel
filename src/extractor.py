from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def has_gps(data: dict):
    pass


def latitude(data: dict):
    pass


def longitude(data: dict):
    pass

def datatime(data: dict):
    pass


def camera_make(data: dict):
    pass


def camera_model(data: dict):
    pass


def dms_to_decimal(dms, ref):
    
    if not dms or not ref:
        return None
    
    try:
        
        degrees = float(dms[0])
        minutes = float(dms[1])
        seconds = float(dms[2])
    except (TypeError, IndexError, ZeroDivisionError):
        return None
    
    # חישוב הנוסחה העשרונית
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    if ref in ['S', 'W', b'S', b'W']:
        decimal = -decimal
    return decimal


def extract_metadata(image_path):
    path = Path(image_path)
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name, "datetime": None, "latitude": None,
            "longitude": None, "camera_make": None, "camera_model": None, "has_gps": False
        }

    
    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        if tag == "GPSInfo":
            for gps_tag_id in value:
                gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                data[gps_tag] = value[gps_tag_id]
        else:
            data[tag] = value

    
    data["latitude"] = dms_to_decimal(data.get("GPSLatitude"), data.get("GPSLatitudeRef"))
    data["longitude"] = dms_to_decimal(data.get("GPSLongitude"), data.get("GPSLongitudeRef"))

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    data_list = []
    fol_path = Path(folder_path)
    for image_path in fol_path.glob("*jpg"):
        data_list.append(extract_metadata(image_path))
    if len(data_list) == 0:
        return 'no images in folder'
    return data_list