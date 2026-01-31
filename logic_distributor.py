import math
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

# إعداد نظام تتبع الأخطاء والعمليات (Logging)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_log.log"),
        logging.StreamHandler()
    ]
)

class Task:
    """تعريف كائن المهمة مع الأولوية والطاقة المطلوبة"""
    def __init__(self, name: str, priority: int, energy_cost: int, duration_min: int):
        self.name = name
        self.priority = priority  # من 1 لـ 5
        self.energy_cost = energy_cost  # 1 (سهلة) لـ 5 (مرهقة)
        self.duration_min = duration_min
        self.is_completed = False

class AdvancedTaskDistributor:
    """
    محرك التوزيع الذكي:
    يعتمد على خوارزمية 'Energy-First Scheduling' لتجنب الإرهاق.
    """
    def __init__(self, monthly_goals: List[Dict], daily_constraints: Dict):
        self.logger = logging.getLogger("TaskDistributor")
        self.raw_goals = monthly_goals
        self.constraints = daily_constraints
        self.days_in_cycle = 30
        self.buffer_time_ratio = 0.15  # 15% وقت طوارئ
        self.schedule = {day: [] for day in range(1, self.days_in_cycle + 1)}
        
        self.logger.info("تم بدء محرك التوزيع بنجاح...")

    def _calculate_total_load(self) -> float:
        """حساب إجمالي ساعات العمل المطلوبة للشهر"""
        total_minutes = sum([g.get('duration', 60) for g in self.raw_goals])
        return total_minutes / 60

    def validate_feasibility(self) -> bool:
        """التأكد من أن الأهداف قابلة للتحقيق واقعياً"""
        available_hours_per_day = self.constraints.get('work_hours_limit', 8)
        total_available = available_hours_per_day * self.days_in_cycle * (1 - self.buffer_time_ratio)
        required = self._calculate_total_load()
        
        if required > total_available:
            self.logger.warning(f"الخطة طموحة جداً! مطلوب {required} ساعة والمتاح {total_available}")
            return False
        return True

    def _prioritize_goals(self):
        """ترتيب الأهداف بناءً على الأولوية والطاقة"""
        # الأولوية العالية والمهام المرهقة تُوضع في البداية (Deep Work)
        return sorted(self.raw_goals, key=lambda x: (x['priority'], x['energy']), reverse=True)

    def distribute(self):
        """توزيع المهام بذكاء على الـ 30 يوم"""
        if not self.validate_feasibility():
            self.logger.error("فشل في التوزيع: الأهداف تتخطى القدرة الزمنية.")
            return None

        sorted_goals = self._prioritize_goals()
        current_day = 1
        day_load_minutes = {day: 0 for day in range(1, 31)}
        max_daily_minutes = self.constraints.get('work_hours_limit', 8) * 60

        for goal in sorted_goals:
            distributed = False
            while not distributed:
                # التأكد من عدم تخطي الحد اليومي
                if day_load_minutes[current_day] + goal['duration'] <= max_daily_minutes:
                    self.schedule[current_day].append({
                        "task_name": goal['name'],
                        "priority": goal['priority'],
                        "energy_level": "High" if goal['energy'] > 3 else "Normal",
                        "status": "scheduled"
                    })
                    day_load_minutes[current_day] += goal['duration']
                    distributed = True
                else:
                    current_day += 1
                    if current_day > 30:
                        self.logger.warning("تم ترحيل بعض المهام للشهر القادم!")
                        break

        self.logger.info("تمت عملية التوزيع بنجاح.")
        return self.schedule

    def get_efficiency_report(self):
        """تقرير تحليل كفاءة الجدول"""
        report = {
            "Total_Hours": self._calculate_total_load(),
            "Daily_Average": self._calculate_total_load() / 30,
            "Complexity_Index": "High" if self._calculate_total_load() > 150 else "Optimal"
        }
        return report

# --- جزء التشغيل التجريبي (Testing) ---
if __name__ == "__main__":
    # مثال لبيانات ضخمة لاختبار الأداء
    goals_data = [
        {"name": f"Task {i}", "priority": (i % 5) + 1, "energy": (i % 3) + 1, "duration": 90}
        for i in range(1, 101)
    ]
    
    user_constraints = {"work_hours_limit": 6}
    
    distributor = AdvancedTaskDistributor(goals_data, user_constraints)
    final_schedule = distributor.distribute()
    
    if final_schedule:
        print(f"تم توزيع {len(goals_data)} مهمة بنجاح.")
        print(f"تقرير الكفاءة: {distributor.get_efficiency_report()}")
