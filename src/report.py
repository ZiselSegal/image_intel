from datetime import datetime

def create_report(map_html, timeline_html, analysis):
  
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # 1. חילוץ נתונים
    date_info = analysis.get("date_range", {})
    start_date = date_info.get("start", "לא ידוע")
    end_date = date_info.get("end", "לא ידוע")
    
    insights_html = "".join([f"<li>{i}</li>" for i in analysis.get("insights", [])])
    if not insights_html:
        insights_html = "<li>לא נמצאו תובנות מיוחדות.</li>"
    
    cameras_html = "".join([f"<span class='badge'>{cam}</span> " for cam in analysis.get("unique_cameras", [])])

    # 2. בניית ה-HTML (f-string)
    html = f"""
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>Image Intel - דוח מודיעין 3D</title>
        <style>
            :root {{
                --primary: #00d2ff;
                --secondary: #3a7bd5;
                --bg: #0f172a;
            }}

            body {{ 
                font-family: 'Segoe UI', sans-serif; 
                background: var(--bg); color: white; margin: 0; 
                padding: 20px 60px; /* הוספת שוליים רחבים יותר בצדדים לנוחות גלילה */
                perspective: 1000px;
            }}

            .header {{ 
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                padding: 40px; border-radius: 15px; text-align: center;
                box-shadow: 0 10px 30px rgba(0,210,255,0.3);
                margin-bottom: 40px;
                transform: translateZ(20px);
            }}

            .section {{ 
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                padding: 30px 50px; /* הגדלת הריווחיות בתוך התיבות */
                margin: 25px 0; border-radius: 15px; 
                border: 1px solid rgba(255,255,255,0.1);
                box-shadow: 0 15px 35px rgba(0,0,0,0.5);
                transition: all 0.4s ease;
            }}

            .section:hover {{
                transform: translateY(-5px) rotateX(2deg); 
                background: rgba(255, 255, 255, 0.1);
            }}

            .stats {{ display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; }}

            .stat-card {{ 
                background: rgba(0, 210, 255, 0.1);
                padding: 20px; border-radius: 12px; text-align: center;
                border: 1px solid var(--primary);
                transition: transform 0.3s;
                flex: 1; min-width: 150px;
            }}

            .stat-card:hover {{
                transform: scale(1.05) translateZ(30px);
                background: var(--primary); color: var(--bg);
            }}

            .stat-number {{ font-size: 2.5em; font-weight: bold; }}

            .badge {{ 
                background: linear-gradient(45deg, var(--primary), var(--secondary));
                color: white; padding: 8px 15px; border-radius: 20px; 
                margin: 5px; display: inline-block; font-weight: bold;
            }}

            /* סטייל לכפתור ההסתרה */
            .toggle-btn {{
                background: linear-gradient(45deg, #2ecc71, #27ae60);
                color: white; border: none; padding: 15px 30px; border-radius: 10px;
                cursor: pointer; font-size: 1.1em; font-weight: bold;
                box-shadow: 0 5px 15px rgba(46, 204, 113, 0.3);
                transition: 0.3s; display: block; margin: 20px auto;
            }}

            .toggle-btn:hover {{ transform: scale(1.05); filter: brightness(1.1); }}

            /* תיבת ציר הזמן המוסתרת */
            #timeline-content {{
                display: none; /* מוסתר בהתחלה */
                padding-top: 20px;
                animation: slideDown 0.5s ease-out;
            }}

            @keyframes slideDown {{
                from {{ opacity: 0; transform: translateY(-20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Image Intel | דוח מודיעין חזותי</h1>
            <p>תאריך הפקה: {now}</p>
        </div>

        <div class="section">
            <h2>📊 סיכום פעילות</h2>
            <div style="background: rgba(0,210,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 20px;">
                <strong>טווח פעילות:</strong> מ-{start_date} עד {end_date}
            </div>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('total_images', 0)}</div>
                    <div>סך תמונות</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('images_with_gps', 0)}</div>
                    <div>עם GPS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(analysis.get('unique_cameras', []))}</div>
                    <div>מכשירים</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>💡 תובנות מהניתוח</h2>
            <ul style="line-height: 1.8;">{insights_html}</ul>
        </div>

        <div class="section">
            <h2>📍 מפת מיקומים</h2>
            <div style="min-height: 400px; border-radius: 10px; overflow: hidden; border: 1px solid var(--primary); shadow: inset 0 0 10px #000;">
                {map_html}
            </div>
        </div>

        <div class="section">
            <h2>⏳ ציר זמן כרונולוגי</h2>
            <button class="toggle-btn" onclick="toggleTimeline()" id="btn-text">הצג ציר זמן מלא</button>
            
            <div id="timeline-content">
                {timeline_html}
            </div>
        </div>

        <div class="section">
            <h2>📱 מכשירים שזוהו</h2>
            <div style="text-align: center;">{cameras_html}</div>
        </div>

        <footer style="text-align:center; padding: 40px; color: rgba(255,255,255,0.3); font-size: 0.9em;">
            &copy; 2026 Image Intel System | Confidential
        </footer>

        <script>
            function toggleTimeline() {{
                var content = document.getElementById("timeline-content");
                var btn = document.getElementById("btn-text");
                if (content.style.display === "block") {{
                    content.style.display = "none";
                    btn.innerText = "הצג ציר זמן מלא";
                    btn.style.background = "linear-gradient(45deg, #2ecc71, #27ae60)";
                }} else {{
                    content.style.display = "block";
                    btn.innerText = "הסתר ציר זמן";
                    btn.style.background = "linear-gradient(45deg, #e74c3c, #c0392b)";
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html

