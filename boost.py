import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8028433138:AAHG7mFHzWiR0QKaMIbRz6v94Ip_d-6zS3E"

TIKTOK_REGEX = re.compile(
    r"https?://(www\.|vm\.|vt\.|m\.)?tiktok\.com/\S+", re.IGNORECASE
)


def download_tiktok(url: str) -> dict | None:
    try:
        res = requests.get(
            "https://www.tikwm.com/api/",
            params={"url": url, "hd": 1},
            timeout=20,
        )
        data = res.json()
        if data.get("code") != 0 or not data.get("data"):
            return None
        info = data["data"]
        return {
            "video_url": info.get("hdplay") or info.get("play"),
            "title": info.get("title", "فيديو تيكتوك"),
            "author": info.get("author", {}).get("nickname", "مجهول"),
        }
    except Exception as e:
        print(f"خطأ في التنزيل: {e}")
        return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك! 👋\n\n"
        "أنا بوت تنزيل تيكتوك بدون علامة مائية 🎬\n\n"
        "فقط أرسل لي رابط أي فيديو تيكتوك وسأرسله لك "
        "مباشرة بجودة عالية وبدون علامة مائية ✅"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 *طريقة الاستخدام:*\n\n"
        "1. افتح تيكتوك\n"
        "2. انسخ رابط أي فيديو\n"
        "3. أرسله هنا\n"
        "4. سأرسل لك الفيديو بدون علامة مائية!\n\n"
        "مثال على رابط صحيح:\n"
        "https://www.tiktok.com/@user/video/123456789",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    chat_id = update.effective_chat.id

    match = TIKTOK_REGEX.search(text)
    if not match:
        await update.message.reply_text(
            "⚠️ الرجاء إرسال رابط تيكتوك صحيح.\n\n"
            "مثال:\nhttps://www.tiktok.com/@user/video/123456789"
        )
        return

    loading = await update.message.reply_text(
        "⏳ جاري تنزيل الفيديو، انتظر قليلاً..."
    )

    result = download_tiktok(match.group(0))

    if not result:
        await loading.edit_text(
            "❌ فشل تنزيل الفيديو. تأكد من أن الرابط صحيح وأن الفيديو ليس خاصاً."
        )
        return

    await loading.edit_text("✅ تم! جاري إرسال الفيديو...")

    try:
        await context.bot.send_video(
            chat_id=chat_id,
            video=result["video_url"],
            caption=(
                f"🎬 *{result['title']}*\n"
                f"👤 {result['author']}\n\n"
                "_بدون علامة مائية ✅_"
            ),
            parse_mode="Markdown",
            supports_streaming=True,
        )
        await loading.delete()
    except Exception as e:
        print(f"خطأ في الإرسال: {e}")
        await loading.edit_text(
            "❌ الفيديو كبير جداً أو حدث خطأ أثناء الإرسال. حاول مرة أخرى."
        )


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ البوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()