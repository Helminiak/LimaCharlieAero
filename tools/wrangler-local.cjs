// The test workspace disallows OS interface enumeration. Use loopback for local
// preview address display. Does not change Cloudflare's assets/routing module.
const os = require('node:os');
os.networkInterfaces = () => ({lo: [{address:'127.0.0.1',netmask:'255.0.0.0',family:'IPv4',mac:'00:00:00:00:00:00',internal:true,cidr:'127.0.0.1/8'}]});
