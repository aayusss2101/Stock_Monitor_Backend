const express=require('express');
const router=express.Router();
const spawn=require('child_process').spawn;
const path=require('path');
const fs=require('fs');
const Decimal=require('decimal.js')

const constants=require('../constants');

const Stock=require('../models/stock');

/**
 * Converts the Value into its Proper Representation
 * 
 * @param {String} value Value of the Field
 * @returns {Decimal/String} Depending on the value of 'value' it returns a string or a decimal
 */
function get_field(value){
  try{
    let base
    if(value.length>1){
      base=Decimal(value.substring(0,value.length-1))
    }
    else
      base=Decimal(value)
    switch(value.charAt(value.length-1)){
      case 'K':base=Decimal.mul(base,1e3)
               break
      case 'M':base=Decimal.mul(base,1e6)
               break
      case 'B':base=Decimal.mul(base,1e9)
               break
      case 'T':base=Decimal.mul(base,1e12)
               break
      default: base=Decimal(value)
    }
    return base
  }catch(err){
    return value
  }
}


/**
 * Converts the JSON data into appropriate format for storage in Database
 * 
 * @param {String} data JSON data scraped
 */
function parse_json(data){
  for(f in data){
    if(typeof(data[f])=="object"){
      parse_json(data[f])
      continue
    }
    data[f]=get_field(data[f])
  }
}



router.post('/', function(req, res, next){

  // Run Python Script
  const pythonProcess=spawn('python', ['scripts/get_data.py', constants.download_path, constants.chrome_webdriver, constants.bse_name, constants.nse_name, constants.file_name])
    
  // Log stdout Stream
  pythonProcess.stdout.on('data', (data)=>{
    console.log(`stdout: ${data}`);
  });

  // Log stderr Stream
  pythonProcess.stderr.on('data', (data)=>{
    console.log(`stderr: ${data}`);
  });

  // Process on Successful Completion of Python Script
  pythonProcess.on('exit', (code)=>{
        
    // Logging Exit Code of Python Script
    console.log(`Process quit with code ${code}`);
        
    /** A {String} File Path of the temporary file where JSON data is stored */ 
    let file_path=path.join(constants.download_path, constants.file_name);
        
    fs.readFile(file_path, function(err, data){
      if(err){
        console.log(err);
        next(err);
      }
            
      let json_data=JSON.parse(data);
      let stocks=json_data.info;

      let options={
        upsert:true,
        setDefaultsOnInsert: true,
      }

      for(let i=0;i<stocks.length;i++){

        parse_json(stocks[i])
        
        /** A {Stock} object containing information from scraped JSON data */
        let stock = new Stock(stocks[i]);

        /** A {String} which serves as the id of the Stock Object */
        let id=stock["Stock Exchange"]+"-"+stock["Ticker Symbol"];
        
        // Removing addToWishlist field from getting updated
        stock.addToWishlist=undefined

        Stock.findOneAndUpdate({_id: id}, stock, options, function(err, res){
          if(err)
            console.error(`Error on saving Stock: ${err}`);
        })
      }
    });

    // Deleting temporary file
    fs.unlink(file_path, (err)=>{
      if(err){
        console.log(err);
        next(err);
      }

      console.log(`${file_path} successfully deleted`);
    });

    res.send("Done");

  });

});

module.exports=router;