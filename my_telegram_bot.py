import subprocess
import os
import cv2
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from secret import Bot_token

# Update your imports for Application
Bot_token = Bot_token
WEBCAM_PHOTO_PATH = "/tmp/webcam_photo.png"
SCREENSHOT_PATH = "/tmp/screenshot.png"

# Function to take a webcam photo
async def webcam_photo(update: Update, context) -> None:
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()

        if ret:
            cv2.imwrite(WEBCAM_PHOTO_PATH, frame)
            await update.message.reply_photo(photo=open(WEBCAM_PHOTO_PATH, 'rb'))
            os.remove(WEBCAM_PHOTO_PATH)
        else:
            await update.message.reply_text("Failed to capture webcam photo.")
    except Exception as e:
        await update.message.reply_text(f"Error capturing webcam photo: {str(e)}")

# Remaining functions (like screenshot, shutdown, etc.) are similar

# Main application logic
async def main() -> None:
    app = ApplicationBuilder().token(Bot_token).build()

    # Add command handlers
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("screenshot", screenshot))
    app.add_handler(CommandHandler("webcam", webcam_photo))

    # Handler for general text commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
