/**
 * Smart Life Architect - Frontend Core Engine
 * نظام إدارة التفاعل، الرسوم البيانية، والربط مع السيرفر
 */

// 1. إعدادات النظام والمتغيرات العامة
const API_BASE_URL = "http://127.0.0.1:5000/api";
let dailyChart = null;

// الانتظار حتى تحميل الصفحة بالكامل
document.addEventListener('DOMContentLoaded', () => {
    console.log("System Initialized...");
    initCharts();
    loadDashboardData();
    setupEventListeners();
});

// 2. إدارة الرسوم البيانية (Charts)
function initCharts() {
    const ctx = document.getElementById('dailyChart').getContext('2d');
    
    // استخدام مكتبة Chart.js لرسم مهام اليوم
    dailyChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['منجز', 'متبقي', 'متأخر'],
            datasets: [{
                data: [0, 100, 0],
                backgroundColor: ['#4facfe', '#16213e', '#ff4b2b'],
                borderWidth: 0
            }]
        },
        options: {
            cutout: '80%',
            responsive: true,
            plugins: { legend: { display: false } }
        }
    });
}

// 3. التعامل مع السيرفر (Fetch API)
async function fetchData(endpoint, method = 'GET', body = null) {
    try {
        const options = {
            method,
            headers: { 'Content-Type': 'application/json' }
        };
        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) throw new Error(`HTTP Error: ${response.status}`);
        return await response.json();
    } catch (error) {
        showNotification("خطأ في الاتصال بالسيرفر", "error");
        console.error("API Error:", error);
    }
}

// 4. منطق الشات بوت (Advanced Chat)
async function sendMessage() {
    const userInput = document.getElementById('userInput');
    const message = userInput.value.trim();
    
    if (!message) return;

    // إضافة رسالة المستخدم للواجهة
    appendMessage('user', message);
    userInput.value = '';

    // إرسال الطلب للسيرفر (البايثون)
    const data = await fetchData('/chat', 'POST', { message });
    
    if (data && data.status === 'success') {
        appendMessage('bot', data.reply);
        // تحديث الواجهة لو الرد فيه تغيير للجدول
        if (data.intent === 'achievement') loadDashboardData();
    }
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById('chatBox');
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}-msg fade-in`;
    msgDiv.innerHTML = `<strong>${sender === 'user' ? 'أنت' : 'المساعد'}:</strong> ${text}`;
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 5. إدارة جدول الـ 30 يوم
async function loadDashboardData() {
    const stats = await fetchData('/stats');
    if (stats) {
        updateProgressUI(stats.success_rate);
        updateChartData(stats.completed_tasks, stats.total_tasks - stats.completed_tasks);
    }
}

function updateProgressUI(percentage) {
    const circle = document.getElementById('monthlyProgress');
    let current = 0;
    const interval = setInterval(() => {
        if (current >= percentage) clearInterval(interval);
        circle.innerText = `${current}%`;
        current++;
    }, 20);
}

function updateChartData(done, pending) {
    dailyChart.data.datasets[0].data = [done, pending, 0];
    dailyChart.update();
}

// 6. التنبيهات والتحسينات البصرية
function showNotification(text, type) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerText = text;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

function setupEventListeners() {
    // إرسال الرسالة عند الضغط على Enter
    document.getElementById('userInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
}
