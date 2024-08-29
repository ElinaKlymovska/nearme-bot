# NearMe Bot

This repository contains the code for a Telegram bot named `GiftForSvetyBot`, developed using Python, Aiogram, and Playwright. The bot leverages web automation and interaction capabilities provided by Playwright.

## Setup and Installation

To get the bot up and running on your server, follow these steps:

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```bash
   git clone https://github.com/ElinaKlymovska/nearme-bot.git
   cd nearme-bot

2. **Set Up a Virtual Environment**

  Create and activate a Python virtual environment:
  
python3 -m venv myenv
source myenv/bin/activate


3. **Install Python Dependencies**

  Install the required Python packages:

pip install -r dependencies/requirements.txt


1. **Install Playwright and System Dependencies**

  Playwright requires additional system dependencies to run. Install these dependencies and download the necessary browsers:

sudo apt-get install libatk1.0-0 libatk-bridge2.0-0 libcups2 libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2 playwright install


1. **Running the Bot**

  Start the bot by running the main.py script:
    
python main.py

    

If you encounter an error related to launching a headed browser, consider running Playwright in headless mode or using xvfb-run:

xvfb-run python main.py
    
This will ensure the bot runs smoothly even on systems without a graphical display.
