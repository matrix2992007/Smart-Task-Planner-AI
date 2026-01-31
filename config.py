# إعدادات النظام الأساسية
APP_NAME = "Smart Life Architect"
VERSION = "1.0.0"

# إعدادات المواعيد الثابتة (الروتين)
DAILY_ROUTINES = {
    "prayers": ["الفجر", "الظهر", "العصر", "المغرب", "العشاء"],
    "gym_session": {
        "duration": "1.5 hours",
        "default_time": "18:00" # الساعة 6 مساءً
    }
}

# إعدادات الذكاء الاصطناعي (الشات بوت)
# هنا بنحط الـ API Key لو استخدمنا OpenAI أو Gemini مستقبلاً
AI_CONFIG = {
    "model": "gpt-4-trained-custom",
    "temperature": 0.7,
    "max_tokens": 150
}

# إعدادات قاعدة البيانات
DB_PATH = "backend/planner_system.db"
