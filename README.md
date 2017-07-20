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

## Motivation

Coding interviews commonly focus on trivial tasks, 'set' problems, how to quicksort.  Here is a quick and dirty script, intented as alternative to evoke more meaningful discussion. About refactoring, and/or extended adding features.   

The following concepts are illustrated.

* Fail Over
* Activity Design  
* Modularity
* Recursion
* Exception handling
* Simple lossless compression 
* Logging 


## How to configure

Edit mongodb credentials

## How to run

python scrape.py

## License

Data access is licensed for personal / educational use.   




