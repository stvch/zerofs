json = require("json");
socket = require( "libfs" );
entries = socket.readdir( ngx.arg[1] );
return (json.encode(entries));
