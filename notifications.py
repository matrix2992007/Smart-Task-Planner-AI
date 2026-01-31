import datetime
import time

class NotificationSystem:
    def __init__(self, db_manager):
        self.db = db_manager

    def check_and_notify(self):
        """
        دالة بتلف على المهام وتشوف إيه اللي ميعاده قرب
        """
        while True:
            # هنفترض إننا بنجيب اليوم الحالي من السيستم
            current_day = 1 
            tasks = self.db.get_day_tasks(current_day)
            
            current_time = datetime.datetime.now().strftime("%H:%M")
            
            for task in tasks:
                task_name, task_type, status = task
                
                # منطق التنبيه الذكي
                if status == 'pending':
                    self.send_alert(task_name, task_type)
            
            # بيفحص كل دقيقة مثلاً (مؤقتاً عشان التجربة)
            time.sleep(60)

    def send_alert(self, task_name, task_type):
        """
        إرسال الإشعار التفاعلي
        """
        if task_type == 'fixed':
            print(f"🔔 تنبيه روتين ثابت: حان موعد {task_name}. لا تؤجل عمل اليوم إلى الغد!")
        else:
            print(f"📅 مهمة من أهداف الشهر: {task_name}. تحب تبدأ فيها دلوقتي؟")

    def interactive_action(self, action, task_id):
        """
        رد الفعل لو المستخدم ضغط على الإشعار (تأجيل / تم)
        """
        if action == "done":
            # تحديث الحالة في قاعدة البيانات
            print(f"عاش! تم تحديث المهمة {task_id} كمنجزة.")
        elif action == "snooze":
            print(f"تم التأجيل لمدة 30 دقيقة. هفكرك تاني.")
