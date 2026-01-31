// 1. منطق الشات بوت (إرسال واستقبال الرسائل)
function sendMessage() {
    const input = document.getElementById('userInput');
    const chatBox = document.getElementById('chatBox');
    
    if (input.value.trim() === "") return;

    // إضافة رسالة المستخدم للواجهة
    chatBox.innerHTML += `<p class="user-msg"><b>أنت:</b> ${input.value}</p>`;
    
    // محاكاة رد السيستم (هنا بيتم الربط مع Python API لاحقاً)
    setTimeout(() => {
        const botResponse = "جاري معالجة طلبك وتعديل الجدول بناءً على رغبتك... ✅";
        chatBox.innerHTML += `<p class="bot-msg" style="color:blue"><b>المساعد:</b> ${botResponse}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }, 1000);

    input.value = "";
}

// 2. تحديث الدوائر والرسوم البيانية (التحليلات)
function updateProgress(percentage) {
    const circle = document.getElementById('monthlyProgress');
    circle.innerText = percentage + "%";
    // ممكن نغير لون الدائرة كل ما النسبة تزيد
    if(percentage > 50) circle.style.borderColor = "#00ff00";
}

// 3. توليد جدول الـ 30 يوم تلقائياً
function generateCalendar() {
    const grid = document.getElementById('calendarGrid');
    for (let i = 1; i <= 30; i++) {
        const dayCard = document.createElement('div');
        dayCard.className = 'stat-card day-item';
        dayCard.innerHTML = `
            <h4>يوم ${i}</h4>
            <button onclick="viewDay(${i})">عرض المهام</button>
        `;
        grid.appendChild(dayCard);
    }
}

function viewDay(day) {
    alert("سيتم جلب مهام اليوم " + day + " من قاعدة البيانات.");
}

// تشغيل الوظائف الأساسية عند تحميل الصفحة
window.onload = () => {
    generateCalendar();
    updateProgress(35); // مثال لنسبة إنجاز أولية
};
