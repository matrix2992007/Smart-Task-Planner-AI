import math

class TaskDistributor:
    def __init__(self, monthly_goals, daily_fixed_routines):
        """
        monthly_goals: قائمة بالأهداف (مثلاً: خلص كتاب، برمجة مشروع)
        daily_fixed_routines: الأشياء الثابتة (صلاة، جيم)
        """
        self.goals = monthly_goals
        self.fixed = daily_fixed_routines
        self.days = 30

    def distribute(self):
        # حساب عدد المهام لكل يوم
        tasks_count = len(self.goals)
        tasks_per_day = math.ceil(tasks_count / self.days)
        
        schedule = {}
        
        for day in range(1, self.days + 1):
            # استخراج مهام اليوم الحالي من القائمة الكبيرة
            start_idx = (day - 1) * tasks_per_day
            end_idx = start_idx + tasks_per_day
            day_tasks = self.goals[start_idx:end_idx]
            
            # دمج المهام المتغيرة مع الروتين الثابت
            schedule[f"Day {day}"] = {
                "Fixed": self.fixed,
                "Dynamic_Tasks": day_tasks,
                "Status": "Pending"
            }
            
        return schedule

# مثال تجريبي لتشغيل السيستم
if __name__ == "__main__":
    my_goals = [f"Goal Number {i}" for i in range(1, 45)] # نفترض عندنا 44 هدف
    my_fixed = ["5 Prayers", "Gym Session"]
    
    planner = TaskDistributor(my_goals, my_fixed)
    result = planner.distribute()
    
    # طباعة أول يوم كمثال
    print("--- Sample Schedule for Day 1 ---")
    print(result["Day 1"])
