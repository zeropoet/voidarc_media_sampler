const Web3 = require('web3');
const providerUrl = 'wss://mainnet.infura.io/ws/v3/YOUR_PROJECT_ID';
const web3 = new Web3(new Web3.providers.WebsocketProvider(providerUrl));
const contractAddress = '0xYourContractAddress';
const abi = [];
const contract = new web3.eth.Contract(abi, contractAddress);

function startListening() {
  console.log('Listening for events...');
  contract.events.allEvents()
    .on('data', (event) => {
      console.log('Event received:', event.event);
      require('./sensoryController').handleEvent(event);
      require('./phiEngine').handleEvent(event);
      require('./archiveManager').handleEvent(event);
    })
    .on('error', console.error);
}

module.exports = { startListening };