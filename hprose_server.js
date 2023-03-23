var hprose = require("hprose");
function ping() {
    var ip = require('ip');
    ip = ip.address()
    var ipStr = String(ip)
    process.stdout.write(ipStr)
    return ipStr;
}
var server = hprose.Server.create("http://0.0.0.0:8080");
server.addFunction(ping);
server.start();