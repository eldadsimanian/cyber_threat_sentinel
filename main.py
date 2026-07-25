import os
import json
import pandas as pd
from dotenv import load_dotenv
from groq import Groq

# טוען את המשתנים מתוך קובץ .env המקומי
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ Missing GROQ_API_KEY! Make sure it is set in your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def load_logs(file_path):
    """טוען את קובץ הלוגים ל-DataFrame של Pandas"""
    return pd.read_csv(file_path)


def detect_brute_force(df, threshold=5):
    """מזהה כתובות IP עם כמות חריגה של ניסיונות התחברות כושלים"""
    return df[df['failed_login_attempts'] >= threshold]


def analyze_threat_with_real_ai(threat_data, threat_type):
    """
    פונה ל-Groq API ושולחת את הנתונים למודל Llama-3 לקבלת תחקיר סייבר בזמן אמת.
    """
    # המרת שורת ה-DataFrame לדיקשנרי
    event_details = threat_data.to_dict()

    # בניית הפרומפט המורכב
    prompt = f"""
    You are an expert Cyber Security SOC Analyst (Tier 1).
    Analyze the following security event and provide a strictly valid JSON response.
    Do NOT include any introduction, explanations, or markdown formatting outside the JSON.

    Event Type: {threat_type}
    Event Details: {event_details}

    Required Output Format (JSON only):
    {{
        "severity": "HIGH / MEDIUM / LOW",
        "attack_vector": "Name of the likely attack",
        "summary": "Short description of what happened",
        "recommended_action": "Immediate step for remediation"
    }}
    """

    try:
        # ביצוע השיגור (API Request) לשרתי Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # מודל AI חזק וחינמי
            messages=[
                {"role": "system",
                 "content": "You are a specialized cybersecurity analyst assistant that outputs only JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2  # נמוך כדי לקבל תשובות מדויקות ולא יצירתיות מדי
        )

        # חילוץ התשובה מה-API
        ai_raw_text = response.choices[0].message.content

        # המרת הטרקסט החוזר (JSON String) לדיקשנרי של Python
        analysis_json = json.loads(ai_raw_text)
        return analysis_json

    except Exception as e:
        print(f"❌ Error communicating with AI API: {e}")
        return None


if __name__ == "__main__":
    print("--- CyberThreat-AI Sentinel (Real API Mode) Started ---\n")

    logs_df = load_logs("network_logs.csv")

    # זיהוי איומים
    brute_force_threats = detect_brute_force(logs_df)

    if not brute_force_threats.empty:
        print("⚠️ Threat Detected! Sending HTTP Request to AI API...\n")

        for index, row in brute_force_threats.iterrows():
            # פנייה ל-API האמיתי!
            analysis = analyze_threat_with_real_ai(row, "Brute Force")

            if analysis:
                print("🤖 [Real AI SOC Analyst Response via API]:")
                print(json.dumps(analysis, indent=4, ensure_ascii=False))
                print("-" * 50)