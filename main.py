#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
نقطة الدخول الرئيسية للبوت
Main entry point
"""

import logging
from bot import app, init_bot
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("🚀 بدء التطبيق من main.py")
    
    PORT = int(os.getenv('PORT', 5000))
    
    init_bot()
    
    logger.info(f"✅ البوت جاهز على المنفذ {PORT}")
    
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=False,
        threaded=True
    )
