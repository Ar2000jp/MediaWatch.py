#!/usr/bin/python

#
# Copyright (C) 2014 Ahmad Draidi
# E-Mail: ar2000jp@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import inotifyx
import Queue
import threading
import subprocess
import os

watchPath = "/home/ar2000jp/Public/"
watchFileName = "list.txt"

mediaPath = "/home/ar2000jp/Music/"
mediaPlayer = "mpv"

def watchFile(fd, queue):
    while (1):
	#print 'wf l'
	inotifyx.get_events(fd)
	if not (os.path.exists(watchPath + watchFileName)):
	    continue
	f = open(watchPath + watchFileName, "r")
	for line in f:
	    for piece in line.strip().split():
		queue.put(piece)
	    #queue.put(line.strip())
	    #print line
	f.close()
	os.remove(watchPath + watchFileName)

def main():
    #print 'm e'
    fd = inotifyx.init()
    queue = Queue.Queue()
    wd = inotifyx.add_watch(fd, watchPath, inotifyx.IN_CLOSE)

    # Start watchFile() thread
    thread = threading.Thread(target=watchFile, args=(fd,queue))
    thread.daemon = True
    thread.start()

    while (1):
	#print 'm l'
	entry = queue.get()
	#print mediaPath + entry
	subprocess.call([mediaPlayer, mediaPath + entry])

    inotifyx.rm_watch(fd, wd)
    os.close(fd)

main()
