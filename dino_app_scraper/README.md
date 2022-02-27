# DapperDino
Software and Tools to support and grow the Dapper Dino NFT community.

# DapperDino Stat Scraper
This tool was made to gather all of the in-game stats into a single source. Warning, this tool is
only as accurate as the dapper dino website. The bugs which exist on the website will directly affect
the accuracy fo this tool.

## Prerequisites
The following must be installed

1. Python
2. Firefox

Install the requirements doc:

`pip install -r requirements.txt`

## Running

Run the following command:

`python3 -m dino_app_scraper`

## Results
The script will create a csv file named dino_stats_final.csv

## Running Tests
`python3 -m unittest discover ./dino_app_scraper/tests`