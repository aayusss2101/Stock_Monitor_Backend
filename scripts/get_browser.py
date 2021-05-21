from selenium import webdriver


def get_browser(download_path, chrome_webdriver_path):
    
    '''
    
    Parameters:
    download_path (String) : Path of the directory to be set as default download directory
    chrome_webdriver_path (String) : Path of the chrome webdriver executable
    
    Returns:
    webdriver : Instance of WebDriver
    
    '''
    
    try:
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless=True
        prefs = {'download.default_directory' : download_path}
        
        chrome_options.add_experimental_option('prefs', prefs)
        
        browser = webdriver.Chrome(chrome_webdriver_path, options=chrome_options)
        
        return browser
    
    except Exception as e:
        print(e)
        raise
        