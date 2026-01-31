import sqlite3
import logging
import os
from datetime import datetime
from threading import Lock

# إعداد الـ Logging الاحترافي
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DB_Manager")

class DatabaseManager:
    """
    نظام إدارة قواعد البيانات المتقدم (Thread-Safe)
    يعتمد على معايير ACID لضمان سلامة البيانات.
    """
    def __init__(self, db_path="planner_system.db"):
        self.db_path = db_path
        self._lock = Lock()  # لضمان عدم حدوث تداخل عند تعدد المهام
        self._initialize_database()

    def _get_connection(self):
        """فتح اتصال آمن مع دعم الـ Foreign Keys"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _initialize_database(self):
        """إنشاء الجداول بنظام العلاقات (Normalization)"""
        with self._lock:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # 1. جدول أهداف الشهر الكبرى
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal_name TEXT NOT NULL,
                    priority INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 2. جدول المهام اليومية (مربوط بالأهداف)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    goal_id INTEGER,
                    day_number INTEGER NOT NULL,
                    task_description TEXT NOT NULL,
                    task_type TEXT CHECK(task_type IN ('fixed', 'dynamic')),
                    status TEXT DEFAULT 'pending',
                    completed_at TIMESTAMP,
                    FOREIGN KEY (goal_id) REFERENCES monthly_goals(id) ON DELETE CASCADE
                )
            ''')

            # 3. جدول سجل المحادثات (لبناء ذاكرة الشات بوت)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    bot_response TEXT,
                    intent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            conn.commit()
            conn.close()
            logger.info("تم تهيئة قاعدة البيانات بنجاح.")

    def add_monthly_goal(self, name, priority):
        """إضافة هدف جديد مع نظام أمان ضد SQL Injection"""
        try:
            with self._lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO monthly_goals (goal_name, priority) VALUES (?, ?)", (name, priority))
                goal_id = cursor.lastrowid
                conn.commit()
                conn.close()
                return goal_id
        except Exception as e:
            logger.error(f"خطأ في إضافة الهدف: {e}")
            return None

    def update_task_status(self, task_id, status):
        """تحديث حالة المهمة وتسجيل وقت الإنجاز"""
        completion_time = datetime.now() if status == 'done' else None
        try:
            with self._lock:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE daily_tasks 
                    SET status = ?, completed_at = ? 
                    WHERE id = ?
                ''', (status, completion_time, task_id))
                conn.commit()
                conn.close()
                return True
        except Exception as e:
            logger.error(f"خطأ في تحديث المهمة: {e}")
            return False

    def get_analytics(self):
        """وظيفة احترافية لحساب الإحصائيات (الدوائر في الـ Frontend)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # حساب الإنجاز الكلي
            cursor.execute("SELECT COUNT(*) FROM daily_tasks")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM daily_tasks WHERE status = 'done'")
            done = cursor.fetchone()[0]
            
            percentage = (done / total * 100) if total > 0 else 0
            
            conn.close()
            return {
                "total_tasks": total,
                "completed_tasks": done,
                "success_rate": round(percentage, 2)
            }
        except Exception as e:
            logger.error(f"خطأ في جلب الإحصائيات: {e}")
            return {"success_rate": 0}

    def save_chat(self, user_msg, bot_msg, intent):
        """حفظ المحادثة لتدريب الـ AI مستقبلاً"""
        with self._lock:
            conn = self._get_connection()
            conn.execute("INSERT INTO chat_history (user_input, bot_response, intent) VALUES (?, ?, ?)",
                         (user_msg, bot_msg, intent))
            conn.commit()
            conn.close()

# --- تجربة النظام ---
if __name__ == "__main__":
    db = DatabaseManager()
    gid = db.add_monthly_goal("تعلم البرمجة المتقدمة", 5)
    print(f"تم إنشاء هدف برقم: {gid}")
    stats = db.get_analytics()
    print(f"معدل الإنجاز الحالي: {stats['success_rate']}%")
