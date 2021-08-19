const express = require('express')
const router = express.Router()
const network = require('../fabric/network')
// const { ensureAuth, ensureGuest } = require('../middleware/auth')
// const User = require('../models/User')
// const jwt = require('jsonwebtoken')


// @desc    Dashboard
// @route   GET /dashboard
router.get('/config', async (req, res) => {
  try {
    res.writeHead(200, {
      'Content-Type': 'application/json-my-attachment',
      "content-disposition": "attachment; filename=\"config.json\""
    });
    res.end(JSON.stringify(req.body))
    // let appname = req.body.application
    // let operation_types = req.body.operations
    // let 
  } catch (err) {
    console.error(err)
    res.render('error/500')
  }
})

router.post('/register_user', async(req,res)=>{
  let response = await network.registerIdentity(req.body.name);
    console.log('response from registerIdentity: ');
    // console.log(response);
    if (response.error) {
      res.send(response.error);
    } else {
        res.json(response)
        // console.log(util.inspect(networkObj));
    }
})



module.exports = router
