from pymongo import MongoClient
import Candlestick
import time 
from time import gmtime, strftime
from urllib.request import Request
from urllib.request import urlopen
from urllib.error import URLError

def getResponse(url):
    req = Request(url)
    r = urlopen(req).read()
    #return json.loads(r.decode('utf-8'))
    return r.decode('utf-8')

import datetime


def main():
    
    attempt = 0
    
    while 1:
        try:            
            catchMainException()            
        except Exception as e:
            LogMessage('main exception, expected every hour on the hour at the weekend, attempt ' + attempt + ' ' + str(e.args))
            if attempt < 3: #0,1,2
                time.sleep(60)
                attempt = attempt + 1
            elif attempt < 4: #3   
                time.sleep(datetime.datetime.now().minute)
                attempt = 1
            elif attempt < 9: #4,5,6,7,8 try 5 times over 5 mins
                time.sleep(60)#60 seconds
                attempt = attempt + 1
            else: #after trying 5 time wait another hour
                attempt = 3 # one more try then wait for rest the of hour       
        #print str(candle.Open) + " " + str(candle.High) + " " + str(candle.Low) #+" " + str(candle.Close) +" " + str(candle.TimeStamp)

def catchMainException():
    
    timeStamp_nextcandle = 0 
    mx=0
    previous = Candlestick.Candles()
    candle = Candlestick.Candles()
    #gapStarted = 0
    gapStartTick = 0
    scrapingStarted = 1
    gapLogInit = 0
    gapCount = 0
    logscrapeemptyStart = 0
	# NB replace with your mongodb credentials
    _client = MongoClient('mongodb://localuser:cleverpass@127.0.0.1:27017/EURUSD')   
    _database=_client.EURUSD
    collection=_database.ticks
    collectio10counter=10
    
    try:    
        while 1:
            responseFromServer = scrapeTick()
            csvItems=responseFromServer.split(",")
            if len(csvItems)==9: 
                logscrapeemptyStart = 0             
                c = "%.5f"%(((float(csvItems[2] + csvItems[3])) + float(csvItems[4] + csvItems[5])) / 2)            
                timeStamp_tick = int(csvItems[1])
                              
                if mx==0:#is this the first tick?
                    if scrapingStarted:
                        scrapingStarted=0
                        LogMessage("Scrape Started: " + GetStringTimefromMillisecondEpoch(timeStamp_tick)) 
                    candle = StartCandleFromTick(timeStamp_tick, c, c) #close value is open and close initially               
                    timeStamp_nextcandle = int(str(timeStamp_tick)[:-3] + "000") + 1000
                    mx=1
                elif timeStamp_tick > candle.TimeStamp:#is this a new tick?
                    gapCount=0
                    if timeStamp_tick < timeStamp_nextcandle:#is this tick within 1s?
                        candle = UpdateCandleWithTick(candle,c)
                    else:
                        if gapLogInit==1:
                            LogMessage("Gap end: " + GetStringTimefromMillisecondEpoch(timeStamp_tick))
                            gapLogInit=0
                        
                        candle.TimeStamp = timeStamp_nextcandle#candle timestamp is the round end second 
                        if candle.Close != previous.Close:
                            MakeMongoConnectSaveOhlcCandle(candle, collection)#close candle
                            if collectio10counter==10:
                                collectio10counter=0
                                MakeMongoConnectSaveOhlcCandle(candle, _database.ticks10)#close candle
                                
                            collectio10counter += 1
                                
                            
                        previous = candle
                        candle = StartCandleFromTick(timeStamp_tick, candle.Close, c)#open is close of previous
                        timeStamp_nextcandle = int(str(timeStamp_tick)[:-3] + "000") + 1000 
                else:
                    gapCount += 1 
                    if gapCount == 1:
                        gapStartTick=timeStamp_tick
                    elif gapCount == 3:#stub candle off, only happens once per gap                
                        if candle.Close != previous.Close:
                            StubCandleOff(timeStamp_nextcandle,candle,collection)
                        previous = candle    
                        candle.Open=candle.Close#next candle open will be close of previous   
                    if gapCount > 270:#30 is a 10 second gap   
                        if gapLogInit == 0:
                            LogMessage("Gap start: " + GetStringTimefromMillisecondEpoch(gapStartTick))
                            gapLogInit=1                  
                    
                time.sleep(0.33333)
            else:
                if logscrapeemptyStart == 0:
                    LogMessage('Scrape response un-scrapable')
                    logscrapeemptyStart = 1 #only one log message per weekend sleep period -- empty scrapes
                time.sleep(60) #wait one minute
    except Exception as e:
        LogMessage('while exception ' + str(e.args))
        

def scrapeTick():
    mx=1
    log=1
    while mx:
        try:
            responseFromServer = getResponse("http://webrates.truefx.com/rates/connect.html?f=csv&c=EUR/USD")#.read()
            return responseFromServer
            break
        except Exception as e:
            if log:
                LogMessage('scrape exception ' + str(e.args))
                log=0         
            time.sleep(0.33333) 
            

def MakeMongoConnectSaveOhlcCandle(candle, collection):    
    #try again every second until there is a connection
    mx=1    
    while mx:
        try:
            collection.insert({'o':candle.Open,
                               'h':candle.High,
                               'l':candle.Low,
                               'c':candle.Close,
                               'dt':candle.TimeStamp
                               }) 
            
            #if isDone == WriteResult.nInserted:
            mx=0
            break
        except Exception as e:
            LogMessage('save ohlccandle exception ' + str(e.args))
            time.sleep(1)        
    

def StubCandleOff(timeStamp_nextcandle,candle,collection):
    collection.insert({'o':candle.Open,
                      'h':candle.High,
                      'l':candle.Low,
                      'c':candle.Close,
                      'dt':timeStamp_nextcandle
                      }) 
    

def GetStringTimefromMillisecondEpoch(milliepoch):
    return datetime.datetime.fromtimestamp(milliepoch/1000).strftime("%Y-%m-%d %H:%M:%S")

def UpdateCandleWithTick(candle, c):
    if c>candle.High: candle.High = c
    if c<candle.Low: candle.Low = c
    candle.Close = c
    return candle
                  
 
def SaveOhlcCandle(candle, collection):
    collection.insert({'o':candle.Open,
                      'h':candle.High,
                      'l':candle.Low,
                      'c':candle.Close,
                      'dt':candle.TimeStamp
                      })   
        
def LogMessage(message):
    with open ('./scrape.log', 'a') as f: f.write (message + " " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) +'\n')
        

def StartCandleFromTick(timeStamp_tick, o, c):
    if o>c:
        h=o
        l=c
    else:
        h=c
        l=o
        
    candle = Candlestick.Candles()
    candle.Open = o
    candle.High = h
    candle.Low = l
    candle.Close = c
    candle.TimeStamp = timeStamp_tick
    return candle           
            
main()

    


