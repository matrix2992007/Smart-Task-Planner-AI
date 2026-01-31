import json
import random
import logging
import os

class AdvancedAI_Assistant:
    def __init__(self, knowledge_base_path="knowledge_base.json"):
        self.logger = logging.getLogger("AIAssistant")
        self.knowledge_base_path = knowledge_base_path
        self.kb = self._load_knowledge_base()
        self.history = []

    def _load_knowledge_base(self) -> dict:
        """تحميل الـ 10,000 كلمة بأمان"""
        if not os.path.exists(self.knowledge_base_path):
            self.logger.error("ملف قاعدة البيانات المعرفية غير موجود!")
            return {}
        with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _detect_intent(self, user_input: str) -> str:
        """
        محرك تحليل النية:
        بيلف على الـ Triggers في الـ 10,000 كلمة ويشوف أنت تقصد إيه
        """
        user_input = user_input.lower()
        for scenario, data in self.kb.get("scenarios", {}).items():
            for trigger in data.get("triggers", []):
                if trigger in user_input:
                    return scenario
        return "general"

    def get_response(self, user_input: str, user_name: str = "يا بطل") -> str:
        """توليد الرد بناءً على التحليل العميق"""
        intent = self._detect_intent(user_input)
        
        # حفظ تاريخ المحادثة (Memory)
        self.history.append({"user": user_input, "intent": intent})
        if len(self.history) > 10: self.history.pop(0)

        if intent in self.kb.get("scenarios", {}):
            responses = self.kb["scenarios"][intent]["responses"]
            response = random.choice(responses)
        else:
            response = "أنا معاك وسامعك، بس وضح لي أكتر عشان أقدر أساعدك في الجدول."

        return response.replace("{name}", user_name)

    def analyze_progress_speech(self, tasks_completed: int):
        """تحليل صوتي (نصي) بناءً على الإنجاز الفعلي"""
        if tasks_completed == 0:
            return "اليوم لسه بيبدأ، يلا بينا أول خطوة هي أصعب خطوة."
        elif tasks_completed > 5:
            return "أداء مذهل! إنت فعلاً ماشي على خطى المحترفين."
        return "بداية كويسة، كمل."

# --- تجربة المحرك ---
if __name__ == "__main__":
    bot = AdvancedAI_Assistant()
    # تجربة رد بناءً على النية
    print(bot.get_response("أنا تعبان جداً ومش هقدر أكمل"))
    print(bot.get_response("تم الإنجاز يا وحش"))
