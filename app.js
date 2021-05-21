let express = require('express');
let path = require('path');
let cookieParser = require('cookie-parser');
let logger = require('morgan');
let mongoose=require('mongoose');

/** A {Router} which serves as the API endpoint for updating the stock list used to scrape data from TradingView */
let updateStockListRouter=require('./routes/update_stock_list');

/** A {Router} which serves as the API endpoint for updating all the Stock objects in the database */
let updateStockDataRouter=require('./routes/update_stock_data');

/** A {Router} which serves as the API endpoint for returning Stock object(s) to the callee */
let getStockDataRouter=require('./routes/get_stock_data');

/** A {Router} which serves as the API endpoint to update the value of the field addToWishlist */
let addToWishlistRouter=require('./routes/add_to_wishlist')

let app = express();

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/stock/update/list', updateStockListRouter);
app.use('/stock/update/data', updateStockDataRouter);
app.use('/stock/get/data', getStockDataRouter);
app.use('/stock/wishlist',addToWishlistRouter);

let mongoDB="mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false";
mongoose.connect(mongoDB, {useNewUrlParser: true, useUnifiedTopology: true, useFindAndModify: false}, function(error){
    if(error)
        console.log(error);
});

let db=mongoose.connection;
db.on("error", console.error.bind(console, "MongoDB Connection Error"));

module.exports = app;