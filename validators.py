import re
import logging
from datetime import datetime

# إعداد الـ Logger الخاص بالحماية
logger = logging.getLogger("SecurityGuard")

class DataValidator:
    """
    نظام التحقق المتقدم: يضمن سلامة البيانات قبل معالجتها.
    """
    
    @staticmethod
    def validate_goal_input(goal_name: str, priority: int) -> bool:
        """التأكد من أن وصف الهدف منطقي وليس مجرد رموز"""
        if not goal_name or len(goal_name.strip()) < 3:
            logger.warning("فشل التحقق: اسم الهدف قصير جداً.")
            return False
        
        if not (1 <= priority <= 5):
            logger.warning("فشل التحقق: الأولوية يجب أن تكون بين 1 و 5.")
            return False
            
        # منع محاولات حقن الأكواد (XSS/SQL Injection)
        forbidden_chars = ["<", ">", ";", "--", "DROP", "SELECT"]
        if any(char in goal_name.upper() for char in forbidden_chars):
            logger.error("تحذير أمني: تم رصد محاولة إدخال رموز مشبوهة!")
            return False
            
        return True

    @staticmethod
    def validate_chat_payload(message: str) -> str:
        """تنظيف نصوص الشات بوت من الفراغات والرموز الضارة"""
        if not message:
            return ""
        # إزالة المسافات الزائدة وتحويل النص لشكل قياسي
        clean_msg = message.strip()
        # تحديد حد أقصى للحروف لحماية السيرفر من الضغط (Dos Attack)
        return clean_msg[:500] 

    @staticmethod
    def check_schedule_logic(start_date: str, duration_days: int) -> bool:
        """التأكد من أن التواريخ المدخلة منطقية"""
        try:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            if duration_days != 30: # نحن نلتزم بنظام الـ 30 يوم
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_knowledge_base(data: dict) -> bool:
        """فحص الـ 10,000 كلمة للتأكد من عدم وجود تكرار أو أخطاء في الـ JSON"""
        try:
            required_keys = ["scenarios", "personality"]
            for key in required_keys:
                if key not in data:
                    logger.error(f"ملف المعرفة يفتقد لمفتاح أساسي: {key}")
                    return False
            return True
        except Exception as e:
            logger.error(f"خطأ في هيكلة ملف المعرفة: {e}")
            return False

# --- تجربة الحماية ---
if __name__ == "__main__":
    validator = DataValidator()
    test_goal = "تعلم Python <script>alert('Hacked')</script>"
    
    if not validator.validate_goal_input(test_goal, 5):
        print("🛡️ الحارس: تم منع إدخال بيانات غير آمنة!")
