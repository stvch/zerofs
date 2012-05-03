json = require("json");
socket = require( "libfs" );
entries = socket.stat( ngx.arg[1] );
return (json.encode(entries));
