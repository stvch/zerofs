Name
======

ZeroFS is a stateless file system over http protocol

Installation
============


Alternatively, `ngx_lua` can be manually compiled into Nginx.

after that, copy the nginx.conf and ngx_lua_scripts into your workspace.


Useage
=======

	zero.py [nginx url base] [remote path] [local path to mount]

example
-------

	zero.py http://localhost /home /tmp/1x


Nginx Compatibility
===================
The module is compatible with the following versions of Nginx:

	*   1.1.x (last tested: 1.1.5)
	*   1.0.x (last tested: 1.0.15)
	*   0.9.x (last tested: 0.9.4)
	*   0.8.x >= 0.8.54 (last tested: 0.8.54)