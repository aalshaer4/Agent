# 1. استخدام نسخة بايثون خفيفة ومستقرة لتسريع البناء وتقليل الحجم
FROM python:3.10-slim

# 2. تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# 3. تحديث النظام وتثبيت أدوات بناء أساسية تحتاجها بعض المكتبات (مثل py_clob_client)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. نسخ ملف المتطلبات أولاً (هذه الخطوة تسرع البناء في المرات القادمة)
COPY requirements.txt .

# 5. تثبيت المكتبات المطلوبة دون الاحتفاظ بملفات الكاش لتخفيف حجم الحاوية
RUN pip install --no-cache-dir -r requirements.txt

# 6. نسخ باقي ملفات المشروع (مثل omni_agent.py وأي ملفات تكوين أخرى)
COPY . .

# 7. الأمر الذي سيتم تنفيذه عند تشغيل الحاوية
CMD ["python", "omni_agent.py"]