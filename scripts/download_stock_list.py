import sys
import os
import time
from selenium.webdriver.support.ui import Select

from get_browser import get_browser


def delete_file(directory, name):

    '''
    
    Parameters:
    directory (String) : Directory of the file to be deleted
    name (String) : Name of the file
    
    '''
    
    file_path=os.path.join(directory, name)
    
    if os.path.isfile(file_path):
        os.remove(file_path)


def get_recent_file(directory):


    '''
    
    Parameters:
    directory (String) : Directory to retrieve the latest file
    
    Returns:
    recent_file (String) : Path of the recent file

    '''
    
    files=[os.path.join(directory,f) for f in os.listdir(directory) if f.endswith(".csv")]
    recent_file=max(files, key=os.path.getctime)
    
    return recent_file


def rename_file(directory, new_name):

    '''
    
    Parameters:
    directory (String) : Directory of the old file
    new_name (String) : Path of the new name for the file
    
    '''
    
    old_name=get_recent_file(directory)
    os.rename(old_name, os.path.join(directory, new_name))
    

def replace_old_file(download_path, file_name):

    '''
    
    Parameters:
    download_path (String) : Path of the default download directory
    file_name (String) : Name of the file to be replaced
    
    '''
    
    delete_file(download_path, file_name)
    rename_file(download_path, file_name)
    

def download_bse_stock_list(browser, download_path, file_name):

    '''
    
    Parameters:
    browser (webdriver) : Instance of WebDriver
    download_path (String) : Path of the default download directory
    file_name (String) : Name of the .csv file containing BSE stocks
    
    '''
    
    try:
        
        bse_url="https://www.bseindia.com/corporates/List_Scrips.aspx"
        browser.get(bse_url)
        
        status=Select(browser.find_element_by_id("ContentPlaceHolder1_ddlStatus"))
        status.select_by_visible_text("Active")
        
        submit=browser.find_element_by_id("ContentPlaceHolder1_btnSubmit")
        submit.click()
        
        download=browser.find_element_by_id("ContentPlaceHolder1_lnkDownload")
        download.click()
        
        time.sleep(5)
            
        replace_old_file(download_path, file_name)
            
    except Exception as e:
        print(e)
        raise
            

def download_nse_stock_list(browser, download_path, file_name):

    '''
    
    Parameters:
    browser (webdriver) : Instance of WebDriver
    download_path (String) : Path of the default download directory
    file_name (String) : Name of the .csv file containing NSE stocks
    
    '''
        
    try:
        
        base_url="https://www.nseindia.com/market-data/securities-available-for-trading"
        browser.get(base_url)
        
        items=browser.find_elements_by_css_selector("a.file.file--mime-application-pdf.file--application-pdf.pdf-download-link")
        items[0].click()
        
        time.sleep(5)
            
        replace_old_file(download_path, file_name)
                
    except Exception as e:
        print(e)
        raise
        

def download_stock_list(download_path, chrome_webdriver, bse_name, nse_name):

    '''
    
    Parameters:
    download_path (String) : Path of the default download directory
    chrome_webdriver (String) : Path of the chrome webdriver executable
    bse_name (String) : Name of the .csv file containing BSE stocks
    nse_name (String) : Name of the .csv file containing NSE stocks

    '''
    
    with get_browser(download_path, chrome_webdriver) as browser:
        
        download_bse_stock_list(browser, download_path, bse_name)
        download_nse_stock_list(browser, download_path, nse_name)
    

if __name__=="__main__":
    download_stock_list(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
