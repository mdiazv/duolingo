# Duolingo

Duolingo is my favorite language learning app! I've used it to learn and improve my french for about one year and a half!
The more I used it, the more I thought of it as an interesting problem in automation and learning.
This project is an experiment which aims to explore how far can I go in modeling an effective solver for the platform.

## Disclaimer

This code and lead to use Duolingo in a way that might be considered cheating. So use it at your own risk.
I don't intend to use it to farm XP, but as an investigation project.
All tests are performed on a new Duolingo account and never on my real account which I use everyday :)

## Requirements

Navigation is powered by selenium webdriver and currently supports Google Chrome, so a working installation of [ChromeDriver](https://chromedriver.chromium.org/downloads) is required

## Running

Until a more decent mechanism is implemented:
```bash
python -m venv .env
. .env/bin/activate
pip install -r requirements.txt
python app/main.py
```
