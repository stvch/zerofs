json = require("json");
local f = io.output(ngx.arg[1]);
f:close()
return(0);
