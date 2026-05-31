#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import asyncio

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

logger.info(f'✅ التوكن موجود')

# إنشء تطبيق Flask
app = Flask(__name__)

# متغيرات عامة
application = None
bot = None
loop = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر البداية"""
    try:
        await update.message.reply_text(
            f"مرحباً! 👋\nأنا بوتك الذكي 🤖"
        )
        logger.info(f"✅ تم الرد على /start من {update.effective_user.first_name}")
    except Exception as e:
        logger.error(f"❌ خطأ في أمر start: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر المساعدة"""
    try:
        help_text = "الأوامر:\n/start - البداية\n/ping - اختبار"
        await update.message.reply_text(help_text)
        logger.info(f"✅ تم الرد على /help")
    except Exception as e:
        logger.error(f"❌ خطأ في أمر help: {e}")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر الاختبار"""
    try:
        await update.message.reply_text("🏓 البوت يعمل! ✅")
        logger.info(f"✅ تم الرد على /ping")
    except Exception as e:
        logger.error(f"❌ خطأ في أمر ping: {e}")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """صدى الرسائل"""
    try:
        await update.message.reply_text(f"📝 قلت: {update.message.text}")
    except Exception as e:
        logger.error(f"❌ خطأ في الصدى: {e}")

async def process_update(update_data):
    """معالجة التحديث من Telegram"""
    try:
        if not application:
            logger.error("❌ التطبيق لم يتم تهيئته")
            return
        
        update = Update.de_json(update_data, bot)
        if update:
            await application.process_update(update)
            logger.info(f"✅ تم معالجة التحديث: {update.update_id}")
        else:
            logger.warning("⚠️ لم يتم إنشاء Update object")
    except Exception as e:
        logger.error(f"❌ خطأ في معالجة التحديث: {e}")

@app.route('/', methods=['GET'])
def index():
    """الصفحة الرئيسية"""
    return {'status': 'Bot is running ✅', 'bot_token': TOKEN[:20] + '...'}, 200

@app.route('/health', methods=['GET'])
def health():
    """فحص صحة التطبيق"""
    return {'status': 'ok'}, 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """معالج webhook من Telegram"""
    try:
        update_data = request.get_json()
        logger.info(f"📨 استقبال رسالة من Telegram: {json.dumps(update_data, ensure_ascii=False)[:100]}")
        
        if update_data:
            # معالجة التحديث باستخدام asyncio
            if loop:
                asyncio.run_coroutine_threadsafe(process_update(update_data), loop)
            else:
                logger.error("❌ لا يوجد event loop")
        
        logger.info("✅ تم الرد بـ OK على Telegram")
        return 'OK', 200
    except Exception as e:
        logger.error(f"❌ خطأ في webhook: {e}")
        return 'ERROR', 500

def init_bot():
    """تهيئة البوت"""
    global application, bot, loop
    
    try:
        logger.info("🚀 جاري تهيئة البوت...")
        
        # إنشاء event loop
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # إنشاء البوت و Application
        bot = Bot(token=TOKEN)
        application = Application.builder().token(TOKEN).build()

        # معالجات الأوامر
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("ping", ping))

        # معالج الرسائل العادية
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

        logger.info("✅ تم تهيئة البوت بنجاح!")
        logger.info(f"✅ البوت متصل برابط: https://api.telegram.org/bot{TOKEN[:20]}...")
        
    except Exception as e:
        logger.error(f"❌ خطأ في تهيئة البوت: {e}")
        raise

if __name__ == '__main__':
    init_bot()
    logger.info(f"🌐 بدء الخادم على المنفذ {PORT}...")
    app.run(host='0.0.0.0', port=PORT, debug=False, threaded=True)
