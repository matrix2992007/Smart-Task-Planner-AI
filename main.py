from logic_distributor import TaskDistributor
from db_manager import DatabaseManager
from ai_assistant import SmartChatBot
from notifications import NotificationSystem

def start_app():
    # 1. تهيئة قاعدة البيانات
    db = DatabaseManager()

    # 2. استقبال المدخلات (دي هتيجي من الـ Frontend لاحقاً)
    monthly_goals = ["برمجة تطبيق", "قراءة كتابين", "تعلم لغة جديدة", "كورس تصميم"]
    fixed_routines = ["الصلاة", "الجيم"]

    # 3. تشغيل الموزع الذكي
    print("⏳ جاري توزيع المهام على 30 يوم...")
    distributor = TaskDistributor(monthly_goals, fixed_routines)
    full_schedule = distributor.distribute()

    # 4. حفظ الجدول في المخزن
    db.save_schedule(full_schedule)
    print("✅ تم حفظ الجدول وتأمين البيانات.")

    # 5. استدعاء الشات بوت
    assistant = SmartChatBot(db)
    
    # تجربة سريعة للشات بوت
    print("\n--- تجربة الشات بوت ---")
    response = assistant.process_request("إيه اللي ورايا النهاردة؟", current_day=1)
    print(f"Assistant: {response}")

    # 6. تشغيل نظام التنبيهات (تجريبي)
    notifier = NotificationSystem(db)
    print("\n🔔 نظام التنبيهات يعمل في الخلفية...")

if __name__ == "__main__":
    start_app()
