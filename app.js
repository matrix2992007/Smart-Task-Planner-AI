from flask import Flask, render_template, request, jsonify, session
from backend.db_manager import DatabaseManager
from backend.logic_distributor import AdvancedTaskDistributor
from backend.ai_assistant import AdvancedAI_Assistant
import logging
import uuid
import os

# إعداد التطبيق
app = Flask(__name__)
app.secret_key = os.urandom(24)  # مفتاح أمان للجلسات

# تهيئة المكونات الأساسية
db = DatabaseManager()
ai = AdvancedAI_Assistant()

# إعداد الـ Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Flask_Server")

# --- Routes (نقاط التواصل) ---

@app.route('/')
def home():
    """الصفحة الرئيسية للتطبيق"""
    return render_template('index.html')

@app.route('/api/generate_schedule', methods=['POST'])
def generate_schedule():
    """توليد جدول الـ 30 يوم من الأهداف المدخلة"""
    try:
        data = request.json
        goals = data.get('goals', [])
        constraints = data.get('constraints', {"work_hours_limit": 8})
        
        # استخدام الموزع المتقدم
        distributor = AdvancedTaskDistributor(goals, constraints)
        full_schedule = distributor.distribute()
        
        if full_schedule:
            # حفظ الأهداف والمهام في قاعدة البيانات
            for day, tasks in full_schedule.items():
                for t in tasks:
                    db.add_monthly_goal(t['task_name'], t['priority'])
            
            return jsonify({
                "status": "success",
                "message": "تم إنشاء الجدول بنجاح",
                "analytics": distributor.get_efficiency_report()
            }), 200
        else:
            return jsonify({"status": "error", "message": "فشل التوزيع، الخطة غير واقعية"}), 400
    except Exception as e:
        logger.error(f"خطأ في توليد الجدول: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """التواصل مع الشات بوت"""
    try:
        user_data = request.json
        user_input = user_data.get('message', '')
        user_id = session.get('user_id', 'Guest')
        
        # جلب الرد من مساعد الـ AI
        bot_response = ai.get_response(user_input)
        intent = ai._detect_intent(user_input)
        
        # حفظ المحادثة في الذاكرة طويلة الأمد
        db.save_chat(user_input, bot_response, intent)
        
        return jsonify({
            "status": "success",
            "reply": bot_response,
            "intent": intent
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": "المساعد يواجه صعوبة حالياً"}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """جلب الإحصائيات لتحديث الدوائر في الواجهة"""
    stats = db.get_analytics()
    return jsonify(stats)

@app.route('/api/update_task', methods=['PATCH'])
def update_task():
    """تحديث حالة مهمة (إنجاز/تأجيل)"""
    data = request.json
    task_id = data.get('task_id')
    new_status = data.get('status')
    
    success = db.update_task_status(task_id, new_status)
    if success:
        return jsonify({"status": "success", "new_progress": db.get_analytics()['success_rate']})
    return jsonify({"status": "error"}), 400

# --- Error Handlers ---
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "المسار غير موجود"}), 404

if __name__ == '__main__':
    # تشغيل السيرفر على الديباج مود للتطوير
    app.run(debug=True, port=5000)
