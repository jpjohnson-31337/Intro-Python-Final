import json
import os
import requests
import csv
from datetime import datetime, timedelta
import time
import sys
from pyfiglet import Figlet
import numpy as np
from colorama import Fore, Style

#Set variables used for tracking stuff in program
loop = True
tickers = []
last_tickers = []
count = 0
y = 0

#Used to ensure date entered for date range is correct
def validateDate(date_string):
    try:
        #Check if input is datetime compatible
        datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        #If the conversion fails, it's not a valid date
        return False

#Does the Mean Reversion Calculations        
def meanReversionStrategy(prices,ticker):
    #Set variables that will be used to determine things
    i = 0
    buying_at = 0
    profit = 0
    first_buy = 0
    
    #Gets the length of the csv, so as to pinpoint the last date of data to determine buy/sell/hold
    with open(f"/home/ubuntu/environment/final_project/data/{ticker}_prices.csv", 'r') as csvData:
            read = csv.reader(csvData)
            length = len(list(read))
  
    #Begin analysing each number in the list
    for price in prices:
        
        current_price = price
    
        #5-day moving average
        if i >= 4:
          avg_price = sum(float(x) for x in prices[i-4:i+1]) / 5
          avg_price = round(avg_price, 2)
        #4-day average
        elif i == 3:
          avg_price = sum(float(x) for x in prices[0:i+1]) / (i + 1)
          avg_price = round(avg_price, 2)
        #3-day average
        elif i == 2:
          avg_price = sum(float(x) for x in prices[0:i+1]) / (i + 1)
          avg_price = round(avg_price, 2)
        #2-day average
        elif i == 1:
          avg_price = sum(float(x) for x in prices[0:i+1]) / (i + 1)
          avg_price = round(avg_price, 2)
        else:
          avg_price = current_price
    
        #Iterator for moving through list
        i += 1
    
        #Determine if stock should be bought
        if current_price < (avg_price * 0.96) and buying_at == 0:
            #Track the first time stock is bought
            if buying_at == 0:
                first_buy = current_price
            else:
                pass
            
            # Update the buying variable
            buying_at = current_price
            # print(f"Buying at: ${buying_at}")
            #set selling variable back to 0
            selling_at = 0
            
            if i == (length - 1):
                saveResults({f"{ticker} Decision_mr" : f"You should BUY this stock today, if you are using the Mean Reversion Strategy."})
            else:
                pass
            
    
        #Determine if stock should/can be sold
        elif current_price > (avg_price * 1.04) and buying_at != 0:
            selling_at = current_price
            #Determine profit from trade
            profit_for_trade = selling_at - buying_at
            #Track total profit
            profit += profit_for_trade
            # print(f"Selling at: ${selling_at}")
            # print(f"Profit: ${round(profit_for_trade, 2)}")
            #Set buying back to 0, as we sold our stock
            buying_at = 0
            
            if (i == length - 1):
                saveResults({f"{ticker} Decision_mr" : f"You should SELL this stock today, if you are using the Mean Reversion Strategy."})
            else:
                pass
      
        else:
            if i == (length - 1):
                saveResults({f"{ticker} Decision_mr" : f"You should HOLD this stock today, if you are using the Mean Reversion Strategy."})
            else:
                pass
    
    #Ensures no divide by 0 errors occur
    if first_buy == 0:
        #Create dictionary with data
        temp_dictionary = {
            f"{ticker}_profit_mr" : f"$0",
            f"{ticker}_returns_mr" : f"0%"
        }
    else:
        #Determine total profit from year  
        tot_return = (profit / first_buy) * 100
        
        #Create dictionary with data
        temp_dictionary = {
            f"{ticker}_profit_mr" : f"${round(profit, 2)}",
            f"{ticker}_returns_mr" : f"{round(tot_return, 2)}%"
        }
    
    #Return needed values
    return temp_dictionary

#Does the Simple Moving Average Calculations      
def simpleMovingAverageStrategy(prices, ticker):
    #Set variables that will be used to determine things
    i = 0
    buying_at = 0
    profit = 0
    first_buy = 0
    
    #Gets the length of the csv, so as to pinpoint the last date of data to determine buy/sell/hold
    with open(f"/home/ubuntu/environment/final_project/data/{ticker}_prices.csv", 'r') as csvData:
            read = csv.reader(csvData)
            length = len(list(read))
    
    #Begin analysing each number in the list
    for price in prices:
        current_price = price
    
        #5-day moving average
        if i >= 4:
          avg_price = sum(float(x) for x in prices[i-4:i+1]) / 5
          avg_price = round(avg_price, 2)
        #4-day average
        elif i == 3:
          avg_price = sum(float(x) for x in prices[0:i+1]) / (i + 1)
          avg_price = round(avg_price, 2)
        #3-day average
        elif i == 2:
          avg_price = sum(float(x) for x in prices[0:i+1]) / (i + 1)
          avg_price = round(avg_price, 2)
        #2-day average
        elif i == 1:
          avg_price = sum(float(x) for x in prices[0:i+1]) / (i + 1)
          avg_price = round(avg_price, 2)
        else:
          avg_price = current_price
    
        #Iterator for moving through list
        i += 1
    
        #Determine if stock should be bought
        if current_price > avg_price and buying_at == 0:
            #Track the first time stock is bought
            if buying_at == 0:
                first_buy = current_price
            else:
                pass
            # Update the buying variable
            buying_at = current_price
            # print(f"Buying at: ${buying_at}")
            #set selling variable back to 0
            selling_at = 0
            
            if i == (length - 1):
                saveResults({f"{ticker} Decision_sma" : f"You should BUY this stock today, if you are using the Simple Moving Average Strategy."})
            else:
                pass
            
            #Determine if stock should/can be sold
        elif current_price < avg_price and buying_at != 0:
            selling_at = current_price
            #Determine profit from trade
            profit_for_trade = selling_at - buying_at
            #Track total profit
            profit += profit_for_trade
            # print(f"Selling at: ${selling_at}")
            # print(f"Profit: ${round(profit_for_trade, 2)}")
            #Set buying back to 0, as we sold our stock
            buying_at = 0
            
            if i == (length - 1):
                saveResults({f"{ticker} Decision_sma" : f"You should SELL this stock today, if you are using the Simple Moving Average Strategy."})
            else:
                pass
      
        else:
            if i == (length - 1):
                saveResults({f"{ticker} Decision_sma" : f"You should HOLD this stock today, if you are using the Simple Moving Average Strategy."})
            else:
                pass
    
    #Ensures no divide by 0 errors occur
    if first_buy == 0:
        #Create dictionary with data
        temp_dictionary = {
            f"{ticker}_profit_sma" : f"$0",
            f"{ticker}_returns_sma" : f"0%"
        }
    else:
        #Determine total profit from year  
        tot_return = (profit / first_buy) * 100
        
        #Create dictionary with data
        temp_dictionary = {
            f"{ticker}_profit_sma" : f"${round(profit, 2)}",
            f"{ticker}_returns_sma" : f"{round(tot_return, 2)}%"
        }
    
    #Return needed values
    return temp_dictionary

#Does the Bollinger Bands Calculations  
def bollingerBandsStrategy(prices, ticker):
    #Set variables that will be used to determine things
    i = 0
    buying_at = 0
    profit = 0
    first_buy = 0
    
    #Gets the length of the csv, so as to pinpoint the last date of data to determine buy/sell/hold
    with open(f"/home/ubuntu/environment/final_project/data/{ticker}_prices.csv", 'r') as csvData:
            read = csv.reader(csvData)
            length = len(list(read))
  
    #Begin analysing each number in the list
    for price in prices:
        current_price = price
    
        #Calculate 7-day moving average
        if i >= 7:
            avg_price = sum(prices[i-19:i+1]) / 20
            avg_price = round(avg_price, 2)
        #Calculate average for initial days
        else:
            avg_price = sum(prices[0:i+1]) / (i + 1)
            avg_price = round(avg_price, 2)
    
        #Iterator for moving through list
        i += 1
    
        #Determine if stock should be bought
        if current_price > (avg_price * 1.05) and buying_at == 0:
            #Track the first time stock is bought
            if buying_at == 0:
                first_buy = current_price
            else:
                pass
        
            # Update the buying variable
            buying_at = current_price
            # print(f"Buying at: ${buying_at}")
            #set selling variable back to 0
            selling_at = 0
            
            if i == (length - 1):
                saveResults({f"{ticker} Decision_bb" : f"You should BUY this stock today, if you are using the Bollinger Bands Strategy."})
            else:
                pass
    
        #Determine if stock should/can be sold
        elif current_price < (avg_price * .95) and buying_at != 0:
            selling_at = current_price
            #Determine profit from trade
            profit_for_trade = selling_at - buying_at
            #Track total profit
            profit += profit_for_trade
            # print(f"Selling at: ${selling_at}")
            # print(f"Profit: ${round(profit_for_trade, 2)}")
            #Set buying back to 0, as we sold our stock
            buying_at = 0
            
            if i == (length - 1):
                saveResults({f"{ticker} Decision_bb" : f"You should SELL this stock today, if you are using the Bollinger Bands Strategy."})
            else:
                pass
      
        else:
            if i == (length - 1):
                saveResults({f"{ticker} Decision_bb" : f"You should HOLD this stock today, if you are using the Bollinger Bands Strategy."})
            else:
                pass
    
    #Ensures no divide by 0 errors occur
    if first_buy == 0:
        #Create dictionary with data
        temp_dictionary = {
            f"{ticker}_profit_bb" : f"$0",
            f"{ticker}_returns_bb" : f"0%"
        }
    else:
        #Determine total profit from year  
        tot_return = (profit / first_buy) * 100
        
        #Create dictionary with data
        temp_dictionary = {
            f"{ticker}_profit_bb" : f"${round(profit, 2)}",
            f"{ticker}_returns_bb" : f"{round(tot_return, 2)}%"
        }
    
    #Return needed values
    return temp_dictionary

#Writes the calculations and prices to the results.json file    
def saveResults(dictionary):
    #define file path for results.json
    json_file_path = "/home/ubuntu/environment/final_project/results.json"
    
    #check if file exists
    if os.path.exists(json_file_path):
        #If exists, append new dictionary to results.json
        with open(json_file_path, 'r') as json_file:
            current_data = json.load(json_file)
        current_data.update(dictionary)
        with open(json_file_path, 'w') as json_file:
            json.dump(current_data, json_file, indent=2)
    else:
        #If it does not exist, write to new file
        with open(json_file_path, 'w') as json_file:
            json.dump(dictionary, json_file, indent=2)

#Gets start and end dates from user
def getDateRange():
    x = True
    
    while x:
        #Let user decided start date
        start_date = input("Please specify a start date for the range of data to be analysed (Use YYYY-MM-DD): ")
        #Checks it is valid input
        if validateDate(start_date) is True:
            #Break loop
            x = False
        else:
            print("Please try again, enter a valid date. (Use YYYY-MM-DD format)\n")
        
    x = True
        
    while x:
        #Let user decided end date
        end_date = input("Please specify an end date for the range of data to be analysed (Use YYYY-MM-DD): ")
        #Checks it is valid input
        if validateDate(end_date) is True:
            #Break loop
            x = False
        else:
            print("Please try again, enter a valid date. (Use YYYY-MM-DD format)\n")
    
    #return desired start and end date
    return start_date, end_date

#Runs prices from all tickers selected through the various trading strategies
def Analysis(tickers):
    #Have each ticker be analyzed
    for ticker in tickers:
        #Get prices for current ticket -- single line was too long, so logic is split on two lines
        prices = [round(float(row[0]), 2) for row in csv.reader(open
            (f"/home/ubuntu/environment/final_project/data/{ticker}_prices.csv", 'r'))]
            
        ##OPTIONAL TO REMOVE CSV FILES##
            #os.remove(f"/home/ubuntu/environment/final_project/data/{ticker}_prices.csv")
        
        #Put current ticker prices into a dictionary and call saveResults function
        saveResults({f"{ticker}_Prices" : prices})
        
        #Combine the dictionaries from sma and mr functions and call saveResults function
        saveResults({**simpleMovingAverageStrategy(prices, ticker), **meanReversionStrategy(prices, ticker), **bollingerBandsStrategy(prices, ticker)})
        
    return None

#Uses Search API to add tickers to list
def getTickers(tickers):
    #API Key
    apiKey = "K56ASNEMVXJY9N9K"
    
    #Have checker variable for loops
    check = True
    
    while check:
        #Ask for a search to be entered
        keyword = input("Search for the stock ticker you would like to analyse (use -1 to exit or 10 to add pre-built list): ")
        #Give the user a way to exit selection
        if keyword == "-1":
            x = ["FILTER1"]
            return x
        
        #Used for simple grading, allows grader to easily load 10 tickers
        elif keyword == '10' and "FILTER" not in tickers:
            tickers = ["ADBE", "AMD", "AAPL", "BRK-A", "COKE", "CRWD", "GOOGL", "NVDA", "RIVN", "YUM", "FILTER"]
            return tickers
        else:
            pass
        
        #Set URL in order to query API for tickers related to that search
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={apiKey}"
        
        #Have the search list variable which we will append tickers to
        search_list = []
        
        #Query API
        try:
            search = requests.get(url)
            data = search.json()
        except:
            print("Error getting data...")
            sys.exit()
        
        #This ensures we still have API requests available, as we have a limit of 25
        if 'Information' in data:
            os.system('clear')
            print(Fore.RED + "Sorry! You are out of API requests for today. Will return you to main menu. Try changing API keys." + Style.RESET_ALL)
            time.sleep(2.5)
            os.system('clear')
            tickers_new = ["FILTER1"]
            return tickers_new
        
        #Check is there is a match for search
        if not data['bestMatches']:
            #There is no match
            print("No matches for that search. Try Again. (Type '-1' to exit)\n")
        else:
            #There is a match
            print("Matching Company Names and Symbols:")
            for match in data["bestMatches"]:
                print(f"{match['2. name']}: {match['1. symbol']}")
                search_list.append(match['1. symbol'])
                check = False
    
    check = True
    
    while check:
        #Ensures the user wants to use on of the matching tickers
        choice = input("Would you like to use one of these tickers(y/n) -> ")
        if choice.upper() == 'Y':
            while check:
                #Displays the options of tickers
                for ticker in search_list:
                    print(ticker)
                
                #Asks for the user to type in the ticker they want to add to list
                ticker = input("Please type one ticker of your choice, how you see it above, to be added to the list of tickers for analysis: ")
                
                #Ensures entry is valid
                if ticker.upper() in search_list and ticker.upper() not in tickers:
                    print("Registering your choice...")
                    time.sleep(.75)
                    check = False
                    os.system('clear')
                    temp_t = [f"{ticker.upper()}"]
                    return temp_t
                    
                elif ticker.upper() in search_list and ticker.upper() in tickers:
                    print("That ticker is already in the list.")
                    return "FILTER1"
                else:
                    print("Incorrect entry, please try again. Could be a typo.")
        
        #If user does not want to use one of the matching tickers, this will send them back to main menu           
        elif choice.upper() == "N":
            print("Sending you back to the main menu.")
            time.sleep(.5)
            check = False
            os.system('clear')
            return "FILTER1"
        #Ensures they can only enter y or n
        else:
            print("Please enter only 'y' or 'n'....Try again." )

#Uses API to get prices for each ticker    
def getPriceData(tickers,start_date,end_date):
    #API Key
    apiKey = "K56ASNEMVXJY9N9K"
    
    #Runs through all tickers selected and gets their price data from the range of dates indicated
    for ticker in tickers:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&outputsize=full&apikey={apiKey}"
        
        json_words = requests.get(url).text
        json_dict = json.loads(json_words)
        
        output_list = []
        
        #The next two sections is to fix/prevent an error that kept randomly heppening
        
        # Check if start_date is already a datetime object
        if isinstance(start_date, datetime):
            # Convert datetime object to string using strftime
            start_date = start_date.strftime('%Y-%m-%d')
        
        # Check if start_date is already a datetime object
        if isinstance(end_date, datetime):
            # Convert datetime object to string using strftime
            end_date = end_date.strftime('%Y-%m-%d')
        
        
        #convert range of dates to datetime format
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        #Gets the closing price from the data gathered
        if "Time Series (Daily)" in json_dict:
            time_series = json_dict["Time Series (Daily)"]
        
            for date_str, data in time_series.items():
                current_date = datetime.strptime(date_str, '%Y-%m-%d')
                if start_date <= current_date <= end_date:
                    output_list.append([data['4. close']])
        
        #Reverses order so calculations are accurate
        output_list.reverse()
        
        #Write prices to CSV file
        csv_filename = f"/home/ubuntu/environment/final_project/data/{ticker}_prices.csv"
        with open(csv_filename, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
        
            for item in output_list:
                csv_writer.writerow(item)
        
        #Gives status message as it writes data to files
        if not output_list:
            print("No data found in the specified date range.")
        else:
            print(Fore.GREEN + f"Data written to {csv_filename}" + Style.RESET_ALL)
    
    time.sleep(.5)
    os.system('clear')
    return None

#Used to find highest performing stock and its profit
def highestPerformer(last_tickers):
    #Opens the results.json for analysis
    with open('/home/ubuntu/environment/final_project/results.json', 'r') as file:
        results = json.load(file)
    
    i = 0
    
    #Runs through list of tickers from last analysis    
    for ticker in last_tickers:
        
        #Gets the keys for the profits from each strategy
        psma = f"{ticker}_profit_sma"
        pmr = f"{ticker}_profit_mr"
        pbb = f"{ticker}_profit_bb"
        
        #Gets the values from each profit
        strat1 = results[psma]
        strat2 = results[pmr]
        strat3 = results[pbb]
        
        #Checks the first ticker and finds the highest result there
        if i == 0:
            highest = max(strat1, strat2, strat3)
            if highest == strat1:
                bstock = ticker
                hstrat = 'Simple Moving Average'
                i = 1
            elif highest == strat2:
                bstock = ticker
                hstrat = 'Mean Reversion'
                i = 1
            else:
                bstock = ticker
                hstrat = 'Bollinger Bands'
                i = 1
        
        #Now compares the first highest to all three results of each ticker, replacing the highest everytime it is dethroned    
        else:
            if highest < strat1:
                highest = strat1
                bstock = ticker
                hstrat = 'Simple Moving Average'
            elif highest < strat2:
                highest = strat2
                bstock = ticker
                hstrat = 'Mean Reversion'
            elif highest < strat3:
                highest = strat3
                bstock = ticker
                hstrat = 'Bollinger Bands'
            else:
                pass
    
    #Returns required info        
    return bstock, highest, hstrat
    
#Displays basic info for the program
def infoPage():
    os.system('clear')
    #This is kind of a dumb page that just explains a little bit about the program
    info = (f"""
Welcome to the {Fore.YELLOW + 'Stock Market Ticker Tool' + Style.RESET_ALL} Information Page. Please read through the short description below and see the {Fore.YELLOW + 'FAQ' + Style.RESET_ALL} for some basic knowledge.
    
    
{Fore.YELLOW + 'Description:' + Style.RESET_ALL} This is a simple project for the DATA 3500 class at Utah State University created by Joseph Johnson. While most everyone who takes this class
does a final project involving the stock market, this project was made to flush out this project based on the basic requirements. Hopefully if you are using
and experiencing this project that you enjoy it and find it interesting.
    
----------------------------------------------------------------------------

{Fore.YELLOW + Figlet(font='starwars').renderText("FAQ") + Style.RESET_ALL}
----------------------------------------------------------------------------
    
{Fore.RED + "Q1:" + Style.RESET_ALL} What API does this program use?

{Fore.GREEN + "A1:" + Style.RESET_ALL} This program uses AlphaVantage's TIME_SERIES_DAILY API and TICKER_SEARCH API.
----------------------------------------------------------------------------

{Fore.RED + "Q2:" + Style.RESET_ALL} Does this program update stock market data in real time?

{Fore.GREEN + "A2:" + Style.RESET_ALL} No. That capability is much too expensive for a simple school project. However, this program could be altered pretty easily* to get that capability.
----------------------------------------------------------------------------

{Fore.RED + "Q3:" + Style.RESET_ALL} Can I look up any stock I want to be analyzed?

{Fore.GREEN + "A3:" + Style.RESET_ALL} Sort of. Any stock ticker that is available through AlphaVantage's SEARCH_UTILITY API can be used.
----------------------------------------------------------------------------

{Fore.RED + "Q4:" + Style.RESET_ALL} Why is this program failing to get data from API?

{Fore.GREEN + "A4:" + Style.RESET_ALL} The current API key, as of writing this is a free API key and is locked to 25 requests per day :(
----------------------------------------------------------------------------

{Fore.RED + "Q5:" + Style.RESET_ALL} Why does this program save pricing data? Couldn't you just use that data for analysis and just output results?

{Fore.GREEN + "A5:" + Style.RESET_ALL} It was a requirement for the assignment...Otherwise, I agree with you random user!

""")
    
    #This makes it type out the page, thought it would be a fun graphic
    for char in info:
        print(char, end='', flush=True)
        time.sleep(0.025)  #Adjust the sleep duration to control the typing speed
    
    print()
    
    #Keeps the text open till the user wants to leave
    exit = input("\nType anything and hit enter to exit: ")
    time.sleep(.05)
    os.system('clear')
    return None

#Can be used to delete results.json file
def cleanUpResults():
    #Removes results.json file
    os.remove('/home/ubuntu/environment/final_project/results.json')

#Can be used to delete price files
def cleanUpPrices():
    folder = '/home/ubuntu/environment/final_project/data'
    
    #lists out contents of a folder
    files = os.listdir(folder)
    
    #Gets each file path for each file in a folder
    for file in files:
        filePath = os.path.join(folder, file)
        if os.path.isfile(filePath):
            #deletes each file path in a given folder
            os.remove(filePath)
            print(f"Successfully deleted: {filePath}")
        else:
            print(f"Unable to delete {filePath}")
        
#Used for cool graphic when loading results
def resultsLoadingScreen():
    #The loading icon characters
    chars = ["|", "/", "-", "\\"]
    
    #Runs the "animatation" for 3 seconds
    sys.stdout.write("Retrieving Results: ")
    for i in range(30):
        time.sleep(0.1)
        sys.stdout.write(chars[i % len(chars)])
        sys.stdout.flush()
        sys.stdout.write("\b")  # Move the cursor back

    sys.stdout.write("\n")
    sys.stdout.flush()

#Used for cool start title screen    
def firstStartTitle():
    #First title word
    text = "Stock"
    fig = Figlet(font='sub-zero')
    ascii_art1 = fig.renderText(text)
    
    #This makes it typed out the title, thought it would be a fun graphic
    for char in ascii_art1:
        print(Fore.GREEN + char + Style.RESET_ALL, end='', flush=True)
        time.sleep(0.01)  #Adjust the sleep duration to control the typing speed
    
    print()
    time.sleep(1)
    #Second title word
    text = "Market"
    fig = Figlet(font='sub-zero')
    ascii_art2 = fig.renderText(text)
    
    #This makes it typed out the title, thought it would be a fun graphic
    for char in ascii_art2:
        print(Fore.GREEN + char + Style.RESET_ALL, end='', flush=True)
        time.sleep(0.01)  #Adjust the sleep duration to control the typing speed
    
    print()
    time.sleep(1)
    #Third title word
    text = "Ticker"
    fig = Figlet(font='sub-zero')
    ascii_art3 = fig.renderText(text)
    
    #This makes it typed out the title, thought it would be a fun graphic
    for char in ascii_art3:
        print(Fore.BLUE + char + Style.RESET_ALL, end='', flush=True)
        time.sleep(0.01)  #Adjust the sleep duration to control the typing speed
    
    print()
    time.sleep(1)
    #Fourth title word
    text = "Tool"
    fig = Figlet(font='sub-zero')
    ascii_art4 = fig.renderText(text)
    
    #This makes it typed out the title, thought it would be a fun graphic
    for char in ascii_art4:
        print(Fore.BLUE + char + Style.RESET_ALL, end='', flush=True)
        time.sleep(0.01)  #Adjust the sleep duration to control the typing speed
    
    print()
    time.sleep(1.5)
    #Main menu description, for first time
    print(Fore.YELLOW + "Welcome to the Stock Market Ticker Tool's Main Menu. Please select an option below to proceed." + Style.RESET_ALL)
    time.sleep(.5)

#This is where the main functions of the program are housed    
def mainFunction(choice, tickers, last_tickers):
    if choice == "1":
        
        #FILTER is used to ensure the list of 10 stocks are not added again. This removes those values as it is not an actual ticker
        if "FILTER" in tickers:
            tickers = [item for item in tickers if item != "FILTER"]
        else:
            pass
        
        if "FILTER1" in tickers:
            tickers = [item for item in tickers if item != "FILTER1"]
        else:
            pass
        
        #Get the start and end date for your desired date range
        start_date, end_date = getDateRange()
        
        #Now using the API get the pricing data for the desired tickers during the desired time
        getPriceData(tickers, start_date, end_date)
        
        #Run the analysis function which will run prices through different strategies and save prices and results to results.json
        Analysis(tickers)
        
        #Save ticker list to last_tickers to aid new analysis, but also allow for the program to read off results from results.json
        last_tickers = tickers
        
        #Reset list of tickers
        tickers = []
        
        os.system('clear')
        
        #Return the last tickers, and tickers to be used elsewhere in program
        return last_tickers, tickers
        
    elif choice == "2":
        #Search for new stock to be added to list of tickers
        tickers_temp = getTickers(tickers)
        
        tickers.extend(tickers_temp)
        
        return tickers
    
    elif choice == "3":
        #Clear screen, for neatness
        os.system('clear')
        
        #Print out current tickers
        
        #Check if any tickers are in the list
        if tickers == []:
            #Message if there are no tickers
            print("No currently selected Stocks, use option 2 to add stocks.")
        else:
            #If there are tickers, print them
            for ticker in tickers:
                print(ticker)
            print(" ")
        time.sleep(2)
        os.system('clear')
        
        return None
        
    elif choice == '4':
        os.system('clear')
        
        #Checks if results.json exists
        if os.path.exists('/home/ubuntu/environment/final_project/results.json'):
            
            #Tries to read results.json file
            try:
                with open('/home/ubuntu/environment/final_project/results.json', 'r') as file:
                    results = json.load(file)
                    
                    #Does a fun loading animation before printing results
                    resultsLoadingScreen()
                    
                    #Loops through last_ticker list of tickers
                    for ticker in last_tickers:
                        print(Fore.GREEN + f"\nResults for {ticker}" + Style.RESET_ALL)
                        time.sleep(1.5)
                        
                        #Preps all the results to be displayed
                        psma = f"{ticker}_profit_sma"
                        rsma = f"{ticker}_returns_sma"
                        pmr = f"{ticker}_profit_mr"
                        rmr = f"{ticker}_returns_mr"
                        pbb = f"{ticker}_profit_bb"
                        rbb = f"{ticker}_returns_bb"
                        
                        #Preps the data for whether or not to buy/sell/hold
                        dsma = f"{ticker} Decision_sma"
                        dmr = f"{ticker} Decision_mr"
                        dbb = f"{ticker} Decision_bb"
                        
                        #Prints out reults for current ticker
                        print(f"{ticker} Simple Moving Average profit: {results[psma]}")
                        time.sleep(.5)
                        print(f"{ticker} Simple Moving Average return: {results[rsma]}")
                        time.sleep(.5)
                        print(f"{ticker} Mean Reversion profit: {results[pmr]}")
                        time.sleep(.5)
                        print(f"{ticker} Mean Reversion return: {results[rmr]}")
                        time.sleep(.5)
                        print(f"{ticker} Bollinger Bands profit: {results[pbb]}")
                        time.sleep(.5)
                        print(f"{ticker} Bollinger Bands return: {results[rbb]}")
                        time.sleep(.5)
                        
                        
                        #These functions are used to grab the results from each strategy, to tell you if you should buy/sell/hold
                        #This section is for simple moving average
                        if 'HOLD' in str({results[dsma]}):
                            print(Fore.YELLOW + results[dsma] + Style.RESET_ALL)
                        elif 'BUY' in str({results[dsma]}):
                             print(Fore.GREEN + results[dsma] + Style.RESET_ALL)
                        else:
                            print(Fore.RED + results[dsma] + Style.RESET_ALL)
                        
                        #This section is for mean reversion
                        if 'HOLD' in str({results[dmr]}):
                            print(Fore.YELLOW + results[dmr] + Style.RESET_ALL)
                        elif 'BUY' in str({results[dmr]}):
                             print(Fore.GREEN + results[dmr] + Style.RESET_ALL)
                        else:
                            print(Fore.RED + results[dmr] + Style.RESET_ALL)
                        
                        #This sections is for bollinger bands
                        if 'HOLD' in str({results[dbb]}):
                            print(Fore.YELLOW + results[dbb] + Style.RESET_ALL)
                        elif 'BUY' in str({results[dbb]}):
                             print(Fore.GREEN + results[dbb] + Style.RESET_ALL)
                        else:
                            print(Fore.RED + results[dbb] + Style.RESET_ALL)
            
            #Catches possible errors            
            except Exception as e:
                print(f"An error occurred while reading the file: {e}")
            
            #Returns all information about which stock and stragey performed the best
            bstock, profit, hstrat = highestPerformer(last_tickers)
            
            #Prints out the best performing metrics
            time.sleep(1.5)
            print(f"\n\nThe overall highest performing stock and strategy for this analysis -> {bstock} using the {hstrat} Strategy: with a profit of {profit}")
            time.sleep(3)
        else:
            #Message if there is not a results.json file
            print("No results file exists yet, please run some analysis first.")
            time.sleep(2)
            
    elif choice == "5":
        #Show the information page
        infoPage()
        
    elif choice == "6":
        loop = True
        #Ends the program loop
        os.system('clear')
        while loop:
            #Asks if they would like to delete the prices data
            clean = input(f"Would you like to {Fore.RED + 'DELETE' + Style.RESET_ALL} the stock prices file(s) (y/n)? ")
            
            if clean.upper() == "Y":
                #Run function to delete them
                cleanUpPrices()
                time.sleep(1.5)
                os.system('clear')
                loop = False
            elif clean.upper() == "N":
                print("The prices files will not be deleted.")
                loop = False
            else:
                #If they do something other than y or n, help them out
                print("Ensure you enter either 'y' for yes or 'n' for no.")
                time.sleep(1.25)
                os.system('clear')
        
        loop = True
        
        while loop:
            #Asks if they would like to delete the results.json file(This helps the program run better next time it runs)
            clean = input(f"Would you like to {Fore.RED + 'DELETE' + Style.RESET_ALL} the results.json file (y/n)? ")
            
            if clean.upper() == "Y":
                #If they want to delete it, check if it exists
                if os.path.exists("/home/ubuntu/environment/final_project/results.json"):
                    #Run function to delete it
                    cleanUpResults()
                    #Give status
                    print("Deleting results.json file.")
                else:
                    #Give message that it does not exist
                    print("results.json does not exist.")
                time.sleep(1.5)
                os.system('clear')
                #Thank them for using the tool
                print("Thank you for using the Stock Market Ticker Tool!")
                time.sleep(2)
                os.system('clear')
                #End program with status message
                print("Sucessfully Ended.")
                exit()
            elif clean.upper() == "N":
                time.sleep(1.5)
                os.system('clear')
                #Thank them for using the tool
                print("Thank you for using the Stock Market Ticker Tool!")
                time.sleep(2)
                os.system('clear')
                #End program with status message
                print("Sucessfully Ended.")
                exit()
            else:
                #If they do something other than y or n, help them out
                print("Ensure you enter either 'y' for yes or 'n' for no.")
                time.sleep(1.25)
                os.system('clear')
    else:
        #If they do something other than a menu option, help them know what to do
        print("\nPlease, try again. Ensure you are only entering '1', '2', '3', '4', '5', or '6'.\n")

#This while loop keeps the program running until the user indicates to close it
while loop:
    #Plays cool start screen, just the first time
    if count == 0:
        firstStartTitle()
        count = 1
    else:
        #Prints regular main menu title screen text
        print(Fore.YELLOW + "\nStock Market Ticker Tool Main Menu. Please select an option below to proceed." + Style.RESET_ALL)
    
    #Asks the user for what they want to do
    choice = input("""
    1. Analyze selected stocks. (Note: This will clear ticker list after analysis.)
    2. Search and add new ticker to list of stocks to be analyzed
    3. Print list of currently selected stock tickers
    4. Read out results from last analysis
    5. Information Page
    6. Close the program
    => """)
    
    #This will get the variable ticker and last_tickers out of this function and into other functions
    if choice == '1' and tickers != []:
        last_tickers, tickers = mainFunction(choice, tickers, last_tickers)
    elif choice == '1' and tickers == []:
        print("Please add some stocks to be analyzed.")
        time.sleep(1.5)
        os.system('clear')
    elif choice == '2':
        tickers = mainFunction(choice, tickers, last_tickers)
    else:
        mainFunction(choice, tickers, last_tickers)
