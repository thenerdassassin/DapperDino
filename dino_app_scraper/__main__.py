# used when we want to run our application directly with python -m dino_app_scraper
from .app import DinoAppScraper

if __name__ == '__main__':
    DinoAppScraper.run()