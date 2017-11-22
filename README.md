# py-fx-scraper
A robust script to scrape real-time FX pair values, stored with up to 80% lossless compression. (Weissmen score 8.7) 

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

## Motivation (Pair programming, coding interviews and whiteboard 'set' problems)

Here is a quick and dirty python3 script. It could use some refactoring, testing, linting, monitoring, backup, training and extending.   

The following concepts are implemented as illustrated.

* Fail Over
* Activity Design  
* Modularity
* Recursion
* Exception handling
* Simple lossless compression (Weissmen score 8.7)
* Logging 
* Out of order filtering (new ticks cannot be out of order when they crash the sub-process, autostart every .33s)
* Event triggering

## How to configure

Edit mongodb credentials

`_client = MongoClient('mongodb://mymongouser:mymongouserpassword@101.111.121.131:27017/EURUSD')`

## How to run

python scrape.py

## License

Data access is licensed for personal / educational use.   

##  [BCH compliance](https://bettercodehub.com/)

- [![BCH compliance](https://bettercodehub.com/edge/badge/Johnpc123/py-fx-scraper?branch=master)](http://practicalcoder.com/).edge-badge-Johnpc123












