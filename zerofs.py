#!/usr/local/bin/python2.7


from collections import defaultdict
from errno import ENOENT
from stat import S_IFDIR, S_IFLNK, S_IFREG
from sys import argv, exit
import time
import stat
from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
import urllib,json
import os

def flag2mode(flags):
    md = {os.O_RDONLY: 'r', os.O_WRONLY: 'w', os.O_RDWR: 'w+'}
    m = md[flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)]
    if flags | os.O_APPEND:
        m = m.replace('w', 'a', 1)
    return m

class MyStat():
    def __init__(self):
	self.st_mode = 0
	self.st_ino = 0
	self.st_dev = 0
	self.st_nlink = 0
	self.st_uid = 0
	self.st_gid = 0
	self.st_size = 0
	self.st_atime = int(time.time())
	self.st_mtime = int(time.time())
	self.st_ctime = int(time.time())

class HTTPFS(LoggingMixIn, Operations):
    def __init__(self,url,remote):
	self.url = url
	self.remote = remote
	self.files = {}	
	
    def getattr(self,path,fhi = None):	
	fname  = os.path.basename(path)
	print fname,path
	st = MyStat()
	if path == '/':
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        elif path.count('/')>=1:
	    print self.remote+path
	    fh = urllib.urlopen(self.url+"/rstat?path="+self.remote+path)
            ct = fh.read()
            ct = json.loads(ct)
	    print ct
	    if (not ct):
		raise FuseOSError(ENOENT)
	    if(ct['type'] == "directory"):
		st.st_mode = stat.S_IFDIR | 0755
            	st.st_nlink = 2 	 
	    else:

	            st.st_mode = stat.S_IFREG | int(ct['mode'])
            st.st_nlink = int(ct['nlink'])
            print "===========================set size=============="
            size=int(ct['size'])
            print "buf length is",size
            st.st_size = size
        else:
            st.st_mode = stat.S_IFDIR | 0755
            st.st_nlink = 2
        return st.__dict__

    def readdir(self, path, fhi):
        print "=======================readdir======================"
        lst=[]
        
        fh = urllib.urlopen(self.url+"/list_dir?path="+self.remote+path)
        ct = fh.read()
        ct = json.loads(ct)
	n = int(ct['n'])
	#print n
	#print ct
	lst = [str(ct.get(str(x))) for x in range(0,n+1)]

	print lst
	return lst
	
    def main(self, *a, **kw):
        self.file_class = None
        return Fuse.main(self, *a, **kw) 

    def read(self, path, size, offset, fhi):
	fh = urllib.urlopen(self.url+"/read?path="+self.remote+path+"&offset="+str(offset)+"&size="+str(size))
        ct = fh.read()
	ct = ct.replace("\\'","'")
        ct = json.loads(ct)
	return ct.encode("utf8")
    
    def chmod(self,path,mode):
	pass
    
    def create(self,path,mode):
	st = MyStat()
	st.st_mode = stat.S_IFREG | mode
	st.size = 0
	fh = urllib.urlopen(self.url+"/rtouch?path="+self.remote+path)
	ct = fh.read()
	return int(ct)

    def getxattr(self, path, name, position=0):
	if (path in self.files):
	    attrs = self.files[path]
        else:
	    self.files[path] = {}
	    attrs = {}
	try:
            return attrs[name]
        except KeyError:
            return ''

    def truncate(self, path, length, fh=None):
	self.files[path]['st_size'] = length

    def unlink(self, path):
	self.files.pop(path)

    def setxattr(self, path, name, value, options, position=0):
	st = self.files[path]
	st[name] = value
	

if __name__ == '__main__':
    fuse = FUSE(HTTPFS(argv[1],argv[2]),argv[3],foreground = True,debug = True)
