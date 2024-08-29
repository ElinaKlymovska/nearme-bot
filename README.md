NearMe Bot
This project contains the code for a Telegram bot called GiftForSvetyBot, built using Python, Aiogram, and Playwright. The bot utilizes various web automation and interaction features provided by Playwright.

Prerequisites
Before running the bot, ensure you have the following installed on your server:

Python 3.8 or later
pip (Python package manager)
Virtual environment (venv)
Git
Setup Instructions
Clone the Repository:

bash
Copy code
git clone https://github.com/ElinaKlymovska/nearme-bot.git
cd nearme-bot
Create and Activate a Virtual Environment:

bash
Copy code
python3 -m venv myenv
source myenv/bin/activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Install Playwright and Download Necessary Browsers:

Playwright is used for browser automation. Install it and download the necessary browsers by running:

bash
Copy code
playwright install
If your system lacks certain dependencies to run Playwright browsers, you may need to install them:

bash
Copy code
sudo playwright install-deps
Run the Bot:

bash
Copy code
python main.py
Note: If you encounter errors related to running a headed browser without an XServer, you can either run Playwright in headless mode or use xvfb-run:

Modify the Playwright launch settings to headless: true in your script.

Or, run the bot using:

bash
Copy code
xvfb-run -a python main.py
