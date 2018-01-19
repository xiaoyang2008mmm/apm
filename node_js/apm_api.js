var express = require('express');
var app = express();
var bodyParser = require('body-parser');

var jsonParser = bodyParser.json();
var MongoClient = require('mongodb').MongoClient;
var DB_CONN_STR = 'mongodb://10.3.2.113:27017/pinpoint';

function sss(name, m_data) {
    var insertData = function(db, name, callback) {
        var collection = db.collection(name);
        collection.insert(m_data,
        function(err, result) {
            if (err) {
                console.log('Error:' + err);
                return;
            }
            callback(result);
        });
    }

    MongoClient.connect(DB_CONN_STR,
    function(err, db) {
        insertData(db, name,
        function(result) {
            db.close();
        });
    });

}

app.post('/api/interface/', jsonParser,
function(req, res) {

    var data = req.body;

    var real_ip = req.get("X-Real-IP") || req.get("X-Forwarded-For") || req.ip;

    var interface_data = data['interface'];
    var dns_data = data['dns'];
    var f = [];
    for (x in interface_data) {
        var inter_obj = interface_data[x];
        inter_obj['range_time'] = parseInt( inter_obj['endTime'] - inter_obj['startTime'] );
        inter_obj['client_ip'] = real_ip;
        f.push(inter_obj);
    }

    sss('interface', f)

    var d = [];
    for (x in dns_data) {
        var dns_obj = dns_data[x];
        dns_obj['range_time'] = parseInt( dns_obj['endTime'] - dns_obj['startTime'] );
        dns_obj['client_ip'] = real_ip;
        d.push(dns_obj);
    }
    sss('dns', d)

    res.end('OK');
})

var server = app.listen(8888,
function() {

    var host = server.address().address
    var port = server.address().port

})
