const express=require('express');
const router=express.Router();
const spawn=require('child_process').spawn;

const constants=require('../constants');

router.post('/', function(req, res, next){

    // Run Python Script
    const pythonProcess=spawn('python', ["scripts/download_stock_list.py", constants.download_path, constants.chrome_webdriver, constants.bse_name, constants.nse_name]);
    
    // Log stdout stream
    pythonProcess.stdout.on('data', (data)=>{
        console.log(`stdout: ${data}`);
    });

    // Log stderr stream
    pythonProcess.stderr.on('data', (data)=>{
        console.log(`stderr: ${data}`);
    });

    // Process on completion of Python Script
    pythonProcess.on('exit', (code)=>{
        console.log(`Process quit with code ${code}`);
        res.send("Received");
    });

});

module.exports=router;