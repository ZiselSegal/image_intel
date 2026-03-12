from extractor import extract_all
from map_view import sort_by_time

def create_timeline(images_data_list):
    # 1. הגדרת משתנה ה-CSS (עיצוב) - שים לב לשימוש ב-f-string
    html_start = f"""
    <div class="timeline-wrapper" style="font-family: 'Segoe UI', sans-serif; max-width: 700px; margin: auto; direction: rtl;">
        <style>
            .timeline-container {{ 
                position: relative; 
                padding-right: 30px; /* שינוי לימין עבור RTL */
                border-right: 3px solid #00d2ff; /* שינוי צבע לכחול הבהיר של הדף */
                border-left: none;
            }}
            .event-card {{ 
                background: rgba(255, 255, 255, 0.05); /* רקע שקוף למחצה כמו ב-section */
                backdrop-filter: blur(10px);
                margin-bottom: 20px; 
                padding: 15px; 
                border-radius: 15px; 
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
                color: white; 
            }}
            .map-btn {{ 
                color: #0f172a !important; 
                background: #00d2ff; 
                padding: 8px 15px; 
                text-decoration: none; 
                border-radius: 8px; 
                font-weight: bold;
                display: inline-block;
                margin-top: 10px;
            }}
            .map-btn:hover {{
                background: #3a7bd5;
                color: white !important;
            }}
        </style>
        <div class="timeline-container">
    """

    # 2. יצירת תוכן הכרטיסים בעזרת לולאה
    cards_html = ""
    for image in images_data_list:
        if image.get('datetime'):
            # פתיחת הכרטיס והכנסת פרטי מכשיר (תמיד קורה)
            cards_html += f"""
    <div class="event-card">
    <div style="color: #007bff; font-weight: bold;">{image['datetime']}</div>
    <div style="margin: 10px 0;">
    <strong>Device:</strong> {image['camera_make']} {image['camera_model']}<br>"""

            # הוספת מיקום רק אם קיים
            if image.get("latitude"):
                cards_html += f"""
    <strong>Location:</strong> {image['latitude']:.4f}, {image['longitude']:.4f}
    </div>
    <a href="https://www.google.com/maps?q={image['latitude']},{image['longitude']}" target="_blank" class="map-btn">
    Open Map
    </a>"""
            else:
                # אם אין מיקום, רק נסגור את הדיב של הטקסט
                cards_html += "</div>"

            # סגירה סופית של ה-event-card
            cards_html += "</div>"

    html_end = """
        </div> </div> """

    return html_start + cards_html + html_end