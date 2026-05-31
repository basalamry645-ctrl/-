#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
from werkzeug.serving import run_simple

# تفعيل السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# الحصول على التوكن من متغيرات البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PORT = int(os.getenv('PORT', 5000))

if not TOKEN:
    logger.error('❌ يجب تعيين متغير البيئة TELEGRAM_BOT_TOKEN')
    raise ValueError('TELEGRAM_BOT_TOKEN not found')

logger.info(f'✅ التوكن موجود: {TOKEN[:20]}...')

# إنشء تطبيق Flask
app = Flask(__name__)

# متغير عام للتطبيق
ptb = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر البداية"""
    try:
        user = update.effective_user
        await update.message.reply_text(
            f"مرحباً {user.first_name}! 👋\n"
            "أنا بوتك الذكي 🤖\n"
            "استخدم /help لمعرفة الأوامر المتاحة"
        )
    except Exception as e:
        logger.error(f"خطأ في أمر start: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر المساعدة"""
    try:
        help_text = (
            "🤖 الأوامر المتاحة:\n"
            "/start - بدء المحادثة\n"
            "/help - عرض هذه الرسالة\n"
            "/ping - اختبار البوت"
        )
        await update.message.reply_text(help_text)
    except Exception as e:
        logger.error(f"خطأ في أمر help: {e}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر الاختبار"""
    try:
        await update.message.reply_text("🏓 البوت يعمل بكفاءة! ✅")
    except Exception as e:
        logger.error(f"خطأ في أمر ping: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """صدى الرسائل"""
    try:
        await update.message.reply_text(f"📝 قلت: {update.message.text}")
    except Exception as e:
        logger.error(f"خطأ في الصدى: {e}")

@app.route('/', methods=['GET'])
def index():
    """الصفحة الرئيسية"""
    return {'status': 'Bot is running ✅'}, 200

@app.route('/health', methods=['GET'])
def health():
    """فحص صحة التطبيق"""
    return {'status': 'ok', 'bot': 'active'}, 200

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """معالج webhook من Telegram"""
    try:
        update_data = request.get_json()
        if update_data:
            update = Update.de_json(update_data, ptb.bot)
            asyncio.run(ptb.process_update(update))
        logger.info("✅ تم معالجة الرسالة بنجاح")
        return 'OK', 200
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة webhook: {e}")
        return 'ERROR', 500

def init_bot():
    """تهيئة البوت"""
    global ptb
    
    logger.info("🚀 جاري تهيئة البوت...")
    
    ptb = Application.builder().token(TOKEN).build()

    # معالجات الأوامر
    ptb.add_handler(CommandHandler("start", start))
    ptb.add_handler(CommandHandler("help", help_command))
    ptb.add_handler(CommandHandler("ping", ping))

    # معالج الرسائل العادية
    ptb.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("✅ تم تهيئة البوت بنجاح!")
    return ptb

if __name__ == '__main__':
    init_bot()
    logger.info(f"🌐 بدء الخادم على المنفذ {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
