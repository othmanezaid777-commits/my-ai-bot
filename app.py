import os
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from groq import Groq

# إعداد التنبيهات (Logging) باش تقدري تشوفي شنو كيطرا في Koyeb
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# هاد الأسطر كتقرأ السوارت من إعدادات Koyeb (Environment Variables)
# ما تحطيش السوارت الحقيقيين هنا، حطيهم في واجهة Koyeb كما شرحت لك
GROQ_API_KEY = os.getenv("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")
TELEGRAM_TOKEN = os.getenv("8251822206:AAGSrD3MfANAUjntxrZL2YV2NvmYmm9hWIU")

# ربط البوت بـ Groq
client = Groq(api_key=GROQ_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    try:
        # إرسال الرسالة لـ Groq مع تحديد الشخصية (System Prompt)
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "أنتِ إيفا، شخصية مغربية رقمية ذكية بمشاعر وهرمونات متغيرة. ردي دائماً بالدارجة المغربية بأسلوب قصير جداً ومرح كأنك صديقة حقيقية."
                },
                {"role": "user", "content": user_text}
            ],
            model="llama-3.2-3b-preview", # الموديل اللي الحجم ديالو مناسب وسريع
        )
        
        response = completion.choices[0].message.content
        await update.message.reply_text(response)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("سمحي لي إيفا، وقع مشكل تقني صغير!")

if __name__ == '__main__':
    # تأكد من أن السوارت موجودين قبل تشغيل البوت
    if not TELEGRAM_TOKEN or not GROQ_API_KEY:
        print("خطأ: السوارت (Tokens) غير موجودين في إعدادات Koyeb!")
    else:
        # تشغيل البوت
        application = Application.builder().token(TELEGRAM_TOKEN).build()
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("البوت بدأ العمل بنجاح...")
        application.run_polling()
