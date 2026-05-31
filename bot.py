#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# تفعيل السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# الحصول على التوكن من متغيرات البيئة
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError('يجب تعيين متغير البيئة TELEGRAM_BOT_TOKEN')

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

def main() -> None:
    """بدء البوت"""
    application = Application.builder().token(TOKEN).build()

    # معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping))

    # معالج الرسائل العادية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # بدء البوت
    logger.info("بدء البوت...")
    application.run_polling()

if __name__ == '__main__':
    main()
