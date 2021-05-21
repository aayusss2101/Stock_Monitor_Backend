/** A {String} which is the path of the directory where temporary files are stored */
const download_path="/home/aayussss2101/Desktop/StockMonitor/data";

/** A {String} which is the path of the Chrome Webdriver */
const chrome_webdriver="/home/aayussss2101/chromedriver";

/** A {String} which is the name of the .csv file containing list of stocks traded on BSE */
const bse_name="BSE_Stock_List.csv";

/** A {String} which is the name of the .csv file containing list of stocks traded on NSE */
const nse_name="NSE_Stock_List.csv";

/** A {String} which is the name of the temporary file where the JSON data to be returned is stored */
const file_name="Json_Data.txt";

module.exports.download_path=download_path;
module.exports.chrome_webdriver=chrome_webdriver;
module.exports.bse_name=bse_name;
module.exports.nse_name=nse_name;
module.exports.file_name=file_name;