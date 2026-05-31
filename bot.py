#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import json

# تفعيل السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# الحصول على التوكن من متغيرات البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PORT = int(os.getenv('PORT', 5000))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-domain.com')

if not TOKEN:
    logger.error('يجب تعيين متغير البيئة TELEGRAM_BOT_TOKEN')
    exit(1)

# إنشء تطبيق Flask
app = Flask(__name__)

# متغيرات عامة
application = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر البداية"""
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.mention_html()}! 👋\n"
        "أنا بوتك الذكي 🤖\n"
        "استخدم /help لمعرفة الأوامر المتاحة"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر المساعدة"""
    help_text = (
        "الأوامر المتاحة:\n"
        "/start - بدء المحادثة\n"
        "/help - عرض هذه الرسالة\n"
        "/ping - اختبار البوت"
    )
    await update.message.reply_text(help_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر الاختبار"""
    await update.message.reply_text("🏓 البوت يعمل بكفاءة!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """صدى الرسائل"""
    await update.message.reply_text(f"قلت: {update.message.text}")

@app.route('/webhook', methods=['POST'])
async def webhook():
    """معالج webhook من Telegram"""
    try:
        update_data = request.get_json()
        update = Update.de_json(update_data, application.bot)
        await application.process_update(update)
        return 'OK', 200
    except Exception as e:
        logger.error(f"خطأ في معالجة الرسالة: {e}")
        return 'ERROR', 500

@app.route('/health', methods=['GET'])
def health():
    """فحص صحة التطبيق"""
    return {'status': 'ok'}, 200

def init_app():
    """تهيئة التطبيق"""
    global application
    
    application = Application.builder().token(TOKEN).build()

    # معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))

    # معالج الرسائل العادية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("تم تهيئة التطبيق بنجاح")

if __name__ == '__main__':
    init_app()
    logger.info(f"بدء البوت على المنفذ {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False)
