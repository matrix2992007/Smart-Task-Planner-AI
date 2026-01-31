import sqlite3

class DatabaseManager:
    def __init__(self, db_name="planner_system.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # إنشاء جدول المهام
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_number INTEGER,
                task_name TEXT,
                task_type TEXT, -- 'fixed' أو 'dynamic'
                status TEXT DEFAULT 'pending'
            )
        ''')
        # إنشاء جدول لحفظ أهداف الشهر الأساسية
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_name TEXT
            )
        ''')
        self.conn.commit()

    def save_schedule(self, schedule):
        """حفظ الجدول الكامل اللي طالع من الـ logic_distributor"""
        for day, content in schedule.items():
            day_num = int(day.split()[1])
            # حفظ المهام الثابتة (صلاة، جيم)
            for f_task in content['Fixed']:
                self.cursor.execute("INSERT INTO tasks (day_number, task_name, task_type) VALUES (?, ?, ?)", 
                                    (day_num, f_task, 'fixed'))
            # حفظ المهام المتغيرة
            for d_task in content['Dynamic_Tasks']:
                self.cursor.execute("INSERT INTO tasks (day_number, task_name, task_type) VALUES (?, ?, ?)", 
                                    (day_num, d_task, 'dynamic'))
        self.conn.commit()

    def get_day_tasks(self, day_num):
        """جلب مهام يوم معين للعرض في التطبيق"""
        self.cursor.execute("SELECT task_name, task_type, status FROM tasks WHERE day_number = ?", (day_num,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
