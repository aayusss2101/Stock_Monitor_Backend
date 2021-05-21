const express=require('express');
const router=express.Router();

const Stock=require('../models/stock');
//const mongoose=require('mongoose');

// Returns all the Stock object in the database
router.post('/', function(req, res, next){
    
    Stock.find()
        .exec(function(err, stock_data_list){
            if(err){
                console.log(err);
                next(err);
                res.send({});
            }
            res.send(stock_data_list);
        })
});

// Returns the Stock object with id==ticker
router.post('/:ticker', function(req, res, next){

    /** A {String} which is the ticker symbol of the Stock object desired */
    const ticker=req.params.ticker;
    
    Stock.findById(ticker,'-__v')
        .exec(function(err, stock_data){
            if(err){
                console.log(err);
                next(err);
                res.send({});
            }
            res.send(stock_data);
        })
});

module.exports=router;