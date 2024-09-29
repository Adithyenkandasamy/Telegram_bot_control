import subprocess
import os
import cv2
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler

Bot_token = "7653707701:AAHuwk3VbWo45XzVEAFysphZC3f564e6-vY"
WEBCAM_PHOTO_PATH = "/tmp/webcam_photo.png"
SCREENSHOT_PATH = "/tmp/screenshot.png"

# Function to take a webcam photo
async def webcam_photo(update: Update, context) -> None:
    try:
        # Capture an image from the webcam
        cap = cv2.VideoCapture(0)  # Open the default camera (camera 0)
        ret, frame = cap.read()  # Capture frame-by-frame
        cap.release()  # Release the webcam

        if ret:
            # Save the captured image
            cv2.imwrite(WEBCAM_PHOTO_PATH, frame)

            # Send the image via Telegram
            await update.message.reply_photo(photo=open(WEBCAM_PHOTO_PATH, 'rb'))

            # Remove the file after sending
            os.remove(WEBCAM_PHOTO_PATH)
        else:
            await update.message.reply_text("Failed to capture webcam photo.")
    except Exception as e:
        await update.message.reply_text(f"Error capturing webcam photo: {str(e)}")

# Function to take a screenshot
async def screenshot(update: Update, context) -> None:
    try:
        # Start Xvfb for headless environments
        subprocess.run("Xvfb :99 -screen 0 1024x768x24 &", shell=True, check=True)
        os.environ['DISPLAY'] = ':99'

        # Use 'import' to take a screenshot
        subprocess.run(f"import -window root {SCREENSHOT_PATH}", shell=True, check=True)
        await update.message.reply_photo(photo=open(SCREENSHOT_PATH, 'rb'))
        os.remove(SCREENSHOT_PATH)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Failed to take screenshot: {e.stderr}")

# Function to shutdown the system
async def shutdown(update: Update, context) -> None:
    try:
        await update.message.reply_text("Shutting down the system...")
        subprocess.run("shutdown now", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Failed to shutdown: {e.stderr}")

# Function to restart the system
async def restart(update: Update, context) -> None:
    try:
        await update.message.reply_text("Restarting the system...")
        subprocess.run("reboot", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Failed to restart: {e.stderr}")

# Function to execute terminal commands
async def reply(update: Update, context) -> None:
    user_message = update.message.text
    try:
        # Execute the terminal command
        result = subprocess.check_output(user_message, shell=True, text=True)
        await update.message.reply_text(f"Command output:\n{result}")
    except subprocess.CalledProcessError as e:
        await update.message.reply_text(f"Error running command: {e}")

def main() -> None:
    app = Application.builder().token(Bot_token).build()

    # Add command handlers for shutdown, restart, screenshot, and webcam photo
    app.add_handler(CommandHandler("shutdown", shutdown))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("screenshot", screenshot))
    app.add_handler(CommandHandler("webcam", webcam_photo))

    # Add handler for general messages (text input for terminal commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    app.run_polling()

if __name__ == "__main__":
    main()
