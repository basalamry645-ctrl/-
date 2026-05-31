#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('8028433138:AAHG7mFHzWiR0QKaMIbRz6v94Ip_d-6zS3E', '8028433138:AAHG7mFHzWiR0QKaMIbRz6v94Ip_d-6zS3E')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! 👋 أنا بوتك الذكي 🤖")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - البداية\n/ping - اختبار")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 البوت يعمل! ✅")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"قلت: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    logger.info("🚀 بدء البوت...")
    app.run_polling()

if __name__ == '__main__':
    main()
