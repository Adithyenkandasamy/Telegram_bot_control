import os
import subprocess
import cv2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from secret import Bot_token  # Make sure you have your token in the secret module

# Define paths for saving images
WEBCAM_PHOTO_PATH = "/tmp/webcam_photo.png"
SCREENSHOT_PATH = "/tmp/screenshot.png"

# Function to take a webcam photo
async def webcam_photo(update: Update, context) -> None:
    try:
        cap = cv2.VideoCapture(0)  # Open the webcam
        ret, frame = cap.read()  # Capture a single frame
        cap.release()

        if ret:
            cv2.imwrite(WEBCAM_PHOTO_PATH, frame)  # Save the captured photo
            await update.message.reply_photo(photo=open(WEBCAM_PHOTO_PATH, 'rb'))  # Send the photo to the user
            os.remove(WEBCAM_PHOTO_PATH)  # Remove the photo after sending
        else:
            await update.message.reply_text("Failed to capture webcam photo.")
    except Exception as e:
        await update.message.reply_text(f"Error capturing webcam photo: {str(e)}")

# Function to shutdown the system
async def shutdown(update: Update, context) -> None:
    await update.message.reply_text("Shutting down...")
    subprocess.call('sudo shutdown now', shell=True)  # Shutdown command for Linux systems

# Function to restart the system
async def restart(update: Update, context) -> None:
    await update.message.reply_text("Restarting...")
    subprocess.call('sudo reboot', shell=True)  # Reboot command for Linux systems

# Function to take a screenshot
async def screenshot(update: Update, context) -> None:
    try:
        screenshot = subprocess.run(["scrot", SCREENSHOT_PATH])  # Using 'scrot' to take a screenshot
        if screenshot.returncode == 0:
            await update.message.reply_photo(photo=open(SCREENSHOT_PATH, 'rb'))  # Send screenshot to user
            os.remove(SCREENSHOT_PATH)  # Remove the screenshot after sending
        else:
            await update.message.reply_text("Failed to capture screenshot.")
    except Exception as e:
        await update.message.reply_text(f"Error capturing screenshot: {str(e)}")

# Function to reply to general text messages
async def reply(update: Update, context) -> None:
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Main application logic
async def main() -> None:
    # Build the Telegram bot application
    app = ApplicationBuilder().token(Bot_token).build()

    # Add command handlers
    app.add_handler(CommandHandler("shutdown", shutdown))  # /shutdown command
    app.add_handler(CommandHandler("restart", restart))    # /restart command
    app.add_handler(CommandHandler("screenshot", screenshot))  # /screenshot command
    app.add_handler(CommandHandler("webcam", webcam_photo))    # /webcam command

    # Handler for general text commands
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))  # Reply to text messages

    # Start polling for updates
    await app.run_polling()

# Run the bot if this script is executed
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
