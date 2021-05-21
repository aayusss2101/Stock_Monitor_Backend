const express=require('express')
const router=express.Router()

const Stock=require('../models/stock')

router.post('/', function(req,res,next){

    /** A {String} which is the id of the Stock object to be updated */
    const id=req.body.id;

    /** A {Boolean} which will be used to send the response to callee */
    const success=true;

    // Finding Stock by 'id'
    Stock.findById(id,function(err,stock){
        
        if(err){
            console.log(`Error finding stock with id: ${id}`);
            success=false
        }
        
        else{
            try{
                stock.addToWishlist=!stock.addToWishlist
                Stock.updateOne({_id:id},stock,function(err,st){
                    if(err){
                        console.log(`Error in updating with id: ${id}`)
                        success=false;
                    }
                })
            }
            catch(e){
                console.log(`error is ${e} and stock is ${stock} and id is ${id}`)
                success=false
            }
        }
    });

    /** A {String} which is sent as a response to the callee */
    let response_msg=success?"success":"fail";
    res.send(response_msg);
});

module.exports=router