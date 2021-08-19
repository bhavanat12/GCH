const express = require('express')
const router = express.Router()
const network = require('../fabric/network')
const path = require('path')

const fs = require('fs');

// let rawdata = fs.readFileSync('../fabric/config.json');
// let config = JSON.parse(rawdata);

var config;
let operations_refer =[]
fs.readFile(path.join(__dirname,'../fabric/config.json'), 'utf8', function (err, data) {
  if (err) throw err;
  config = JSON.parse(data);
  config.operations.forEach(i => {
      operations_refer[i.operation_name] = i.operation_type
    // if( i.operation_name == operation ) operation_type = i.operation_type
});
});

router.post('/submit', async(req,res)=>{
    let networkObj = await network.connectToNetwork(req.body.name);

    if (networkObj.error) {
        res.send(networkObj.error);
    }
    let operation = req.body.operation
    // let operation_type = ''
    let data={}
    // config.operations.forEach(i => {
    //     if( i.operation_name == operation ) operation_type = i.operation_type
    // });
    console.log(operations_refer[operation])
    if (operations_refer[operation] == 'create' || 'update'){
        data = {
            appname:config.application.application_id,
            key: req.body.key,
            operation_name:operation,
            hash: req.body.data
        }
    }
    else if(operations_refer[operation] == 'delete'){
        data = {
            appname:config.application.application_id,
            key: req.body.key,
        }
    }
    let args = [JSON.stringify(data)];
    console.log(args)

    let invokeResponse = await network.invoke(networkObj, false, operations_refer[operation]+'Operation', args);
    if (invokeResponse.error) {
        res.send(invokeResponse.error);
    }
    res.json("Succesfully Updated")
})

router.get('/query/:id',async(req,res)=>{
    let query = req.params.id.split('=')
    // res.send(query.split("="))
    let networkObj = await network.connectToNetwork('admin');
    let query_type = query[0]
    let query_data = query[1]
    let response = await network.invoke(networkObj, true, 'queryBy'+query_type, query_data);
    let parsedResponse = await JSON.parse(response);
    res.send(parsedResponse);
})

// router.post('/queryByKey', async (req, res) => {
//     // console.log('req.body: ');
//     // console.log(req.body);
  
//     let networkObj = await network.connectToNetwork(req.body.name);
//     // console.log('after network OBj');
//     let response = await network.invoke(networkObj, true, 'readMyAsset', req.body.key);
//     response = JSON.parse(response);
//     if (response.error) {
//       console.log('inside eRRRRR');
//       res.send(response.error);
//     } else {
//       console.log('inside ELSE');
//       res.send(response);
//     }
//   });

  router.get('/queryAll', async (req, res) => {

    let networkObj = await network.connectToNetwork('admin');
    let response = await network.invoke(networkObj, true, 'queryAll', '');
    let parsedResponse = await JSON.parse(response);
    res.send(parsedResponse);
  
  });

  router.get('/getHistory/:id', async(req,res)=>{
    let key = req.params.id
    let networkObj = await network.connectToNetwork('admin');
    let response = await network.invoke(networkObj, true, 'getTransactionHistory', key);
    let parsedResponse = await JSON.parse(response);
    res.send(parsedResponse);

  })

module.exports = router
