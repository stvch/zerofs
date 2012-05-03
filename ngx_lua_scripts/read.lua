json = require("json");
local f = io.open(ngx.arg[1]);
local fh = f:seek("cur",tonumber(ngx.arg[2]));
local ds = f:read(tonumber(ngx.arg[3]));
f:close()
return(json.encode(ds));
