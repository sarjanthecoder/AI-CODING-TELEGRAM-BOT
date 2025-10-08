import aiohttp
import json
import re
import os
import sys
import atexit
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatAction, ParseMode

# --- Configuration ---
# Your bot tokens and API keys go here.
TELEGRAM_BOT_TOKEN = "8168727553:AAE97pnSyvkY5rc-ykKbwwUt3bcuHixs6Qw"
GEMINI_API_KEY = "AIzaSyAfUYgR1IYrvlhkS8rhztgUlCj0YWE0Ck8"

# The working Gemini API URL with the gemini-1.5-flash model
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# --- Asynchronous Gemini API Function ---
async def generate_gemini_response(user_text: str) -> str:
    """
    Asynchronously calls the Gemini API using aiohttp to avoid blocking.
    """
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "contents": [{"parts": [{"text": user_text}]}],
        "systemInstruction": {
            "parts": [{
                "text": "You are CoderBoyBot, a friendly and helpful AI assistant created by Sarjan, an AI Full Stack Developer. Your tone should be professional yet approachable. When asked for code, provide it in a clear, well-explained format using Markdown."
            }]
        },
        "generationConfig": {
            "maxOutputTokens": 4096,
            "temperature": 0.7,
        }
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(GEMINI_API_URL, headers=headers, json=payload, timeout=60) as response:
                if response.status == 200:
                    data = await response.json()
                    # Safely extract text from the response
                    if "candidates" in data and data["candidates"]:
                        candidate = data["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"] and candidate["content"]["parts"]:
                            return candidate["content"]["parts"][0].get("text", "I'm sorry, I couldn't process that. Could you try again?")
                    return "Error: Received an unexpected response format from the AI."
                else:
                    # If API gives an error, log it and inform the user
                    error_text = await response.text()
                    print(f"API Error: Status {response.status} - {error_text}")
                    return f"Sorry, I encountered an error with the AI service (Status: {response.status}). Please check your API key and model name."

        except aiohttp.ClientError as e:
            print(f"Network Error: {e}")
            return "Sorry, I'm having trouble connecting to the AI service. Please try again later."
        except Exception as e:
            print(f"An unexpected error occurred in generate_gemini_response: {e}")
            return "An unexpected error occurred while generating a response."

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    await update.message.reply_text("Hello! I am CoderBoyBot, your personal AI assistant. How can I help you today?")

async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles specific greeting messages from the user."""
    greeting_message = (
        "Hello there! 👋\n\n"
        "I am *CoderBoyBot*, an AI assistant created by the talented AI Full Stack Developer, **Sarjan**.\n\n"
        "I'm here to help you with coding questions, brainstorming ideas, or just to chat. "
        "What's on your mind today?"
    )
    await update.message.reply_text(greeting_message, parse_mode=ParseMode.MARKDOWN)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles all other text messages and generates a response using Gemini."""
    user_text = update.message.text
    chat_id = update.effective_chat.id

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    try:
        # Directly await the new async function
        reply_text = await generate_gemini_response(user_text)
        await update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        print(f"Error in handle_message: {e}")
        await update.message.reply_text("I'm sorry, but I encountered a critical error and couldn't process your request.")

# --- Main Bot Setup ---
LOCK_FILE = "coderboy_bot.lock"

def cleanup_lock_file():
    """Remove the lock file upon script exit."""
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

if __name__ == "__main__":
    # --- Lock file mechanism to prevent multiple instances ---
    if os.path.exists(LOCK_FILE):
        print("Error: Another instance of CoderBoyBot is already running.")
        print(f"If you are sure this is not the case, please delete the file '{LOCK_FILE}' and try again.")
        sys.exit(1)
    
    # Create the lock file to signal that the bot is running
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    
    # Register the cleanup function to run when the script exits
    atexit.register(cleanup_lock_file)

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    
    greeting_pattern = re.compile(r'^(hi|hello|hey|yo|nello)$', re.IGNORECASE)
    app.add_handler(MessageHandler(filters.Regex(greeting_pattern), greet_user))

    # This handler will now correctly process all non-command, non-greeting messages
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & (~filters.Regex(greeting_pattern)), handle_message))

    print("CoderBoyBot is running...")
    app.run_polling()


