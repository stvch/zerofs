zerofs
======

ZeroFS is a stateless file system over http protocol

Installation
============


Nginx Lua Module
-----------------

Alternatively, `ngx_lua` can be manually compiled into Nginx:

1. Install LuaJIT 2.0 (Recommended) or Lua 5.1 (Lua 5.2 is *not* supported yet). Lua can be obtained free from the [the LuaJIT download page](http://luajit.org/download.html) or [the standard Lua homepage](http://www.lua.org/).  Some distribution package managers also distribute Lua and LuaJIT.
1. Download the latest version of the ngx_devel_kit (NDK) module [HERE](http://github.com/simpl/ngx_devel_kit/tags).
1. Download the latest version of this module [HERE](http://github.com/chaoslawful/lua-nginx-module/tags).
1. Download the latest version of Nginx [HERE](http://nginx.org/) (See [Nginx Compatibility](http://wiki.nginx.org/HttpLuaModule#Nginx_Compatibility))

Build the source with this module:


    wget 'http://nginx.org/download/nginx-1.0.15.tar.gz'
    tar -xzvf nginx-1.0.15.tar.gz
    cd nginx-1.0.15/
 
    # tell nginx's build system where to find lua:
    export LUA_LIB=/path/to/lua/lib
    export LUA_INC=/path/to/lua/include
 
    # or tell where to find LuaJIT when if using JIT instead
    # export LUAJIT_LIB=/path/to/luajit/lib
    # export LUAJIT_INC=/path/to/luajit/include/luajit-2.0
 
    # Here we assume Nginx is to be installed under /opt/nginx/.
    ./configure --prefix=/opt/nginx \
            --add-module=/path/to/ngx_devel_kit \
            --add-module=/path/to/lua-nginx-module
 
    make -j2
    make install


after these steps, copy the nginx.conf and ngx_lua_scripts into your workspace.


Useage
=======

zero.py [nginx url base] [remote path] [local path to mount]

example
=======

zero.py http://localhost /home /tmp/1x
