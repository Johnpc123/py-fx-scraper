# py-fx-scraper
A robust script to scrape real-time FX pair values, stored with up to 80% lossless compression.  

## Overview

This activity is performed to monitor real time FX spot data, available by http. Stored as 60s OHLC candles. 

        class Candles(object):
            def __init__(self):
                self.Open = 0
                self.Low = 0
                self.High = 9
                self.Close = 0
                self.TimeStamp = 0
            pass   

![](FXScrapeActivityDiagram.png?raw=true)

## Motivation: Robust automatic continuous real time data monitoring.

Here is a quick python3 script.   

With,

* Fail Over
* Activity Design  
* Modularity
* Recursion
* Exception handling
* Efficiency
* Simple lossless compression 
* Logging 
* Out of order filtering (new ticks cannot be out of order when they crash the sub-process, autostart every .33s)
* Event triggering

## How to configure

Install mongoDB

Edit mongodb credentials

`_client = MongoClient('mongodb://mymongouser:mymongouserpassword@101.111.121.131:27017/EURUSD')`

`python3 -m pip install pymongo`

## How to run

`python3 scrape.py`

## License

Data access is licensed for personal / educational use.   














