import folium
import os
import base64
from io import BytesIO
from PIL import Image


def get_base64_image(image_path, size=(150, 150)):
    """המרת תמונה ל-Base64 כדי שתוצג ב-Popup ללא בעיות אבטחה של נתיבים"""
    try:
        if not image_path or not os.path.exists(image_path):
            return None
        with Image.open(image_path) as img:
            img.thumbnail(size)
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            return base64.b64encode(buffered.getvalue()).decode()
    except Exception:
        return None


def sort_by_time(arr):
    arr.sort(key=lambda x: x.get('datetime') or "")
    return arr


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.
    """
    gps_images = [img for img in images_data if img.get("has_gps")]

    if not gps_images:
        return """
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; 
                    height: 500px; color: white; background: rgba(255, 255, 255, 0.03); 
                    border-radius: 15px; text-align: center; border: 1px dashed rgba(255,255,255,0.1);">
            <div style="font-size: 60px; margin-bottom: 20px; opacity: 0.5;">📍</div>
            <h2 style="font-size: 36px; margin: 0; font-weight: bold; letter-spacing: 1px;">No GPS Data Found</h2>
            <p style="font-size: 18px; opacity: 0.6; margin-top: 10px;">האנלייזר לא מצא מידע גאוגרפי בתמונות שנסרקו.</p>
        </div>
        """

    # חישוב מרכז המפה
    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    # מילון הצבעים לפי מכשיר (מהקוד המקורי שלך)
    device_colors = {
        "Samsung": "blue",
        "Apple": "red",
        "Xiaomi": "orange",
        "Huawei": "green",
        "Google": "purple",
        "OnePlus": "pink",
        "Sony": "darkred",
        "Oppo": "cadetblue"
    }

    # הוספת מרקרים
    for img in gps_images:
        color = device_colors.get(img.get("camera_make"), "gray")

        # הכנת התמונה ל-Popup (משתמש ב-full_path שיצרנו ב-extractor)
        encoded_img = get_base64_image(img.get('full_path'))

        if encoded_img:
            img_html = f'<img src="data:image/jpeg;base64,{encoded_img}" style="width:150px; border-radius:5px; margin-bottom:5px;">'
        else:
            img_html = '<div style="width:150px; height:100px; background:#ddd; border-radius:5px; display:flex; align-items:center; justify-content:center; color:#666; margin-bottom:5px;">No Image</div>'

        popup_text = f"""
        <div style="text-align: center; font-family: 'Segoe UI', sans-serif; width: 160px;">
            {img_html}<br>
            <b style="font-size: 14px;">{img.get('filename', '')}</b><br>
            <span style="font-size: 12px; color: #555;">
                {img.get('datetime', '')}<br>
                {img.get('camera_model', '')}
            </span>
        </div>
        """

        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=folium.Popup(popup_text, max_width=200),
            icon=folium.Icon(color=color)
        ).add_to(m)

    with_time = [img for img in gps_images if img.get("datetime")]
    if len(with_time) > 1:
        sorted_images = sort_by_time(with_time)
        line_points = [[img["latitude"], img["longitude"]] for img in sorted_images]

        folium.PolyLine(line_points, color="purple", weight=3, opacity=0.7).add_to(m)

    return m._repr_html_()