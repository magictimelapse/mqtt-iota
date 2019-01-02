const MAM = require('mam.node.js')
const IOTA = require('iota.lib.js')
const moment = require('moment')
const MQTT = require('mqtt')

/// iota part ///
//const iota_host = 'http://localhost:14265'
const iota_host = 'https://durian.iotasalad.org:14265'
const MODE = 'public' // set to public, restricted or private
const SIDEKEY = ''
const iota = new IOTA({provider: iota_host})
const SECURITYLEVEL = 2 // 1, 2 or 3

let mamState = MAM.init(iota, undefined, SECURITYLEVEL)

if (MODE == 'restricted') {
    const key = iota.utils.toTrytes(SIDEKEY);
    mamState = MAM.changeMode(mamState, MODE, key);
} else {
    mamState = MAM.changeMode(mamState, MODE);
}


const publish = async function(packet) {
    console.log('publishing message... ')
    console.log(packet)
    const trytes = iota.utils.toTrytes(JSON.stringify(packet));
    const message = MAM.create(mamState, trytes);
    console.log("root: ", message.root)
    mamState = message.state;
    transaction = MAM.attach(message.payload, message.address);
    await transaction;
    return message.root;
}


/// mqtt part ///
var mqtt_subscriber = MQTT.connect({
    host: 'localhost',
    port: 1883})

mqtt_subscriber.on('connect', function() {
    mqtt_subscriber.subscribe('sensors/data', function(err) {
	if(!err) {
	    console.log('connected and subscribed to mqtt sensors/data stream');
	}
    })
})

mqtt_subscriber.on('message', function(topic, message) {
    obj = JSON.parse(message);
    const root = publish(obj);
})

process.on('uncaughtException', function (exception) {
    console.log(exception);
});



