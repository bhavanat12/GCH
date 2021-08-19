const path = require('path');
const fs = require('fs');

const configPath = path.join(process.cwd(), './config_blockchain.json');
const configJSON = fs.readFileSync(configPath, 'utf8');
const config = JSON.parse(configJSON);

const appAdmin = config.appAdmin;

module.exports=appAdmin