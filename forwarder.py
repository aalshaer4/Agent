from pyrogram import Client, filters
from anthropic import AsyncAnthropic
import asyncio

# ==========================================
# 1. إعدادات المفاتيح (تيليغرام و كلود)
# ==========================================
TELEGRAM_API_ID = 6
TELEGRAM_API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"     # ضع الـ API_HASH الخاص بتيليغرام
CLAUDE_API_KEY = "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"      # ضع مفتاح Claude الخاص بك هنا

# ==========================================
# 2. إعدادات القنوات
# ==========================================
SOURCE_CHANNELS = ["@Alibk3" , "@ajMubasher"]  # القنوات التي سنسحب منها الأخبار
DESTINATION_CHANNEL = "@your_news_channel" # قناتك التي سينشر فيها الخبر

# تهيئة عملاء تيليغرام وكلود
app = Client("news_session", api_id=TELEGRAM_API_ID, api_hash=TELEGRAM_API_HASH)
claude_client = AsyncAnthropic(api_key=CLAUDE_API_KEY)

# ==========================================
# 3. تعليمات المحرر (System Prompt)
# ==========================================
# هذه هي نفس التعليمات التي كتبناها سابقاً باللغة الإنجليزية لضمان أفضل فهم
EDITOR_INSTRUCTIONS = """
You are a professional and objective news editor. Your task is to take the following raw news text and rewrite it to be ready for publishing on a news Telegram channel, strictly adhering to the following conditions:

1. Draft an engaging, direct, and easy-to-read news post.
2. Remove any links, source channel names, or advertisements present in the original text.
3. Add a short and prominent headline in the first line (use double asterisks **for bolding**).
4. Maintain the strict accuracy of information, names, and numbers without any falsification or hallucination.
5. Try to summarize and shorten the news as much as possible while fully preserving its core context and meaning.
6. When reporting statements or quotes: Place the person's name on a separate line by itself, skip two lines, and then write the exact text of the statement.
"""

# ==========================================
# 4. دالة الاستماع والمعالجة
# ==========================================
@app.on_message(filters.chat(SOURCE_CHANNELS) & filters.text)
async def process_news(client, message):
    raw_news = message.text
    print("\n" + "="*40)
    print(f"📥 [خبر جديد] تم السحب، جاري المعالجة عبر Claude...")
    
    try:
        # إرسال الخبر إلى Claude لإعادة الصياغة
        # نستخدم موديل Haiku لأنه الأسرع والأرخص وممتاز جداً للأخبار
        response = await claude_client.messages.create(
            model="claude-3-haiku-20240307", 
            max_tokens=1000,
            system=EDITOR_INSTRUCTIONS,
            messages=[
                {"role": "user", "content": f"Here is the raw news:\n\n{raw_news}"}
            ]
        )
        
        # استخراج النص المُعاد صياغته
        rewritten_news = response.content[0].text
        print("🧠 [Claude] تمت إعادة الصياغة بنجاح! جاري النشر...")
        
        # نشر الخبر في قناتك
        await client.send_message(DESTINATION_CHANNEL, rewritten_news)
        print("✅ تم النشر في القناة!")
        
    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")

# ==========================================
# 5. تشغيل البوت
# ==========================================
if __name__ == "__main__":
    print("🚀 جاري تشغيل رادار الأخبار مع الذكاء الاصطناعي (Claude)...")
    app.run()
