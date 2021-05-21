import os
import sys
import time
import json
import pandas as pd
import numpy as np

from get_browser import get_browser


def get_url(ticker):

    '''

    Parameters:
    ticker (String) : Ticker of the stock

    Returns:
    String: URL of the stock
    
    '''
    
    base_url="https://in.tradingview.com/symbols/"
    return base_url+ticker



def get_stock_data_section(section):

    '''
    
    Parameters: 
    section (webdriver) : Section in the information about the stock

    Returns:
    section_name (String) : Name of the section
    section_info (Dict) : Dictionary containing information about the section
    
    '''
    
    try:
        section_name=section.find_element_by_class_name("tv-widget-fundamentals__title").text
        
        section_info={}
        
        entries=section.find_elements_by_class_name("tv-widget-fundamentals__row")
        
        length=len(entries)
        
        for i in range(length):
            entry=entries[i].text
            label_value_pair=entry.splitlines()
            section_info[label_value_pair[0]]=label_value_pair[1]
        
        return section_name, section_info
        
    except Exception as e:
        raise e


def get_stock_data(browser, ticker):

    '''
    
    Parameters:
    browser (webdriver) : Instance of WebDriver
    ticker (String) : Ticker of the stock
    
    Returns:
    info (Dict) : Dictionary containing information about the stock
    None if an error occurs
    
    '''

    
    try:
        
        browser.get(get_url(ticker))
        
        time.sleep(1.0)
        
        info={}
        
        name=browser.find_elements_by_class_name("tv-symbol-header__first-line")
        info["Company Name"]=name[1].text
        
        sections=browser.find_elements_by_class_name("tv-widget-fundamentals__item")
        
        length=len(sections)
        
        for i in range(length):
            section_name, section_info=get_stock_data_section(sections[i])
            info[section_name]=section_info
            
        return info
    
    except Exception as e:
        print(f'{ticker} -> {e}')
    
    return None
    

def get_exchange_info(download_path, chrome_webdriver, base_symbol, ticker_list):


    '''
    
    Parameters:
    download_path: Path of the default download directory
    chrome_webdriver (String) : Path of the chrome webdriver executable
    base_symbol (String) : Symbol of the stock exchange
    ticker_list (List) : List containing all the tickers in the exchange
    
    Returns:
    data (List) : List of dictionary containing information of the stocks
    
    '''
    
    data=[]
    
    with get_browser(download_path, chrome_webdriver) as browser:
        
        for ticker in ticker_list:
            
            info=get_stock_data(browser, base_symbol+ticker)
            
            if info==None:
                continue
            
            info["Stock Exchange"]=base_symbol[:3]
            info["Ticker Symbol"]=ticker
            
            data.append(info)
    
    return data
            

def get_bse_data(download_path, chrome_webdriver, file_name):

    '''
    
    Parameters:
    download_path (String) : Path of the default download directory
    chrome_webdriver (String) : Path of the chrome webdriver executable
    file_name (String) : Name of the .csv file containing BSE stocks
    
    Returns:
    bse_data (List) : List containing the data of the NSE stocks
    
    '''
    
    file_path=os.path.join(download_path, file_name)
    
    data=pd.read_csv(file_path)
    ticker_list=data["Security Id"]
    ticker_list=np.array(ticker_list)
    
    base_symbol="BSE-"
    
    bse_data=get_exchange_info(download_path, chrome_webdriver, base_symbol, ticker_list)
    
    return bse_data
                

def get_nse_data(download_path, chrome_webdriver, file_name):


    '''
    
    Parameters:
    download_path (String) : Path of the default download directory
    chrome_webdriver (String) : Path of the chrome webdriver executable
    file_name (String) : Name of the .csv file containing NSE stocks
    
    Returns:
    nse_data (List) : List containing the data of the NSE stocks
    
    '''
    
    file_path=os.path.join(download_path, file_name)
    
    data=pd.read_csv(file_path)
    ticker_list=data["SYMBOL"]
    ticker_list=np.array(ticker_list)
    
    base_symbol="NSE-"
    
    nse_data=get_exchange_info(download_path, chrome_webdriver, base_symbol, ticker_list)
    
    return nse_data
                

def get_data(download_path, chrome_webdriver, bse_name, nse_name, file_name):

    '''
    
    Parameters:
    download_path (String) : Path of the default download directory
    chrome_webdriver (String) : Path of the chrome webdriver executable
    bse_name (String) : Name of the .csv file containing BSE stocks
    nse_name (String) : Name of the .csv file containing NSE stocks
    file_name (String) : Name of the output file containing json data
    
    '''

    
    data=[]
    
    bse_data=get_bse_data(download_path, chrome_webdriver, bse_name)
    nse_data=get_nse_data(download_path, chrome_webdriver, nse_name)
    
    data.extend(bse_data)
    data.extend(nse_data)
    
    json_data={}
    json_data["info"]=data
    
    with open(os.path.join(download_path, file_name), 'w') as json_file:
        json.dump(json_data, json_file)
        


if __name__=="__main__":
    get_data(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])