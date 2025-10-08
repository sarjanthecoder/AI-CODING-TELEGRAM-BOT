CoderBoyBot - A Gemini-Powered Telegram Bot


🚀 About This Project
CoderBoyBot is an intelligent and professional Telegram bot designed to be your personal AI assistant. Powered by Google's advanced Gemini 1.5 Flash model, this bot can engage in natural conversations, answer coding questions, brainstorm ideas, and much more.

This project was created by the talented AI Full Stack Developer, Sarjan, to demonstrate a robust, asynchronous, and user-friendly bot architecture.

✨ Features
Intelligent Conversations: Leverages the power of Google's Gemini AI for human-like and context-aware responses.

Asynchronous Architecture: Built with aiohttp to handle API requests without freezing, ensuring the bot is always responsive.

Professional User Experience: Includes features like a "typing..." indicator and custom-scripted greetings.

Advanced Error Handling: Intelligently reports specific API or network errors (e.g., safety blocks, connection issues) instead of crashing or staying silent.

Markdown Support: Formats responses, especially code snippets, in clean and readable Markdown.

Singleton Instance Lock: A professional lock file mechanism prevents multiple instances of the bot from running, avoiding common conflicts.

🛠️ Setup and Installation
Follow these steps to get your own instance of CoderBoyBot up and running.

1. Prerequisites
Python 3.8 or higher

A Telegram Bot Token from BotFather

A Gemini API Key from Google AI Studio

2. Clone the Repository
First, get the code by cloning this repository or downloading the files.

git clone <your-repository-url>
cd <your-repository-directory>

3. Install Dependencies
The bot relies on a few Python libraries. Install them using pip:

pip install python-telegram-bot aiohttp

4. Configure Your Bot
Open the coderboy_bot.py file and replace the placeholder tokens with your actual keys:

# --- Configuration ---
# Your bot tokens and API keys go here.
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

▶️ How to Run the Bot
Once the setup is complete, you can start the bot from your terminal:

python coderboy_bot.py

If everything is configured correctly, you will see the message CoderBoyBot is running.... You can now go to Telegram and start chatting with your bot!

To stop the bot, simply press Ctrl + C in the terminal. The lock file will be cleaned up automatically.

👤 Creator
This project was developed with ❤️ by Sarjan.
portfolio: www.sarjan.site