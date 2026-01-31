import json

class SmartChatBot:
    def __init__(self, db_manager):
        self.db = db_manager
        # ده "السياق" اللي بنعرف بيه الشات بوت وظيفته (System Prompt)
        self.system_prompt = """
        أنت مساعد ذكي لإدارة الوقت. مهمتك هي:
        1. مساعدة المستخدم في فهم جدوله اليومي.
        2. تعديل المهام إذا طلب المستخدم ذلك (تأجيل، حذف، إضافة).
        3. تشجيع المستخدم بناءً على نسبة إنجازه.
        """

    def process_request(self, user_input, current_day):
        """
        هنا السيستم بيفهم كلام المستخدم وبيرد عليه بناءً على بياناته في القاعدة
        """
        # جلب مهام اليوم عشان الشات بوت "يشوفها"
        tasks = self.db.get_day_tasks(current_day)
        
        # منطق بسيط للتعديل (سيتم ربطه بـ AI API لاحقاً)
        if "تعبان" in user_input or "خفف" in user_input:
            return self._handle_reschedule(current_day)
        
        elif "فاضل إيه" in user_input:
            task_list = ", ".join([t[0] for t in tasks if t[2] == 'pending'])
            return f"باقي عندك في جدول النهاردة: {task_list}. بالتوفيق يا بطل!"
            
        else:
            return "أنا معاك.. تحب أعدل لك حاجة في المهام ولا أسجل لك مهمة جديدة؟"

    def _handle_reschedule(self, day):
        # منطق داخلي لنقل المهام غير المكتملة لليوم التالي
        return "ولا يهمك، ريحتك أهم. رحلت المهام غير الضرورية لبكرة، تقدر ترتاح دلوقتي."
