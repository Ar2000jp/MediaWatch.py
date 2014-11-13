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
import time
import shlex

watchPath = "/home/ar2000jp/Public"
watchFilePrefix = "cap"

mediaPath = "/home/ar2000jp/Music"
mediaPlayer = "mpv"
mediaPlayerParams = "--no-terminal"

readDelay = 2
eventTimeout = 10

def watchFiles(queue):
    mediaFound = False
    fd = inotifyx.init()
    wd = inotifyx.add_watch(fd, watchPath, inotifyx.IN_CLOSE)

    while (1):
	# Wait for an event with timeout.
	event = inotifyx.get_events(fd, eventTimeout)
	print("Event caught, or timed-out.")

	# Wait before reading files
	time.sleep(readDelay)

	for fname in os.listdir(watchPath):
	    fpath = os.path.join(watchPath, fname)
	    if os.path.isfile(fpath) and fname.startswith(watchFilePrefix):
		mediaFound = False
		print ("Processing file: " + fpath)
		f = open(fpath, "r")

		for line in f:
		    pieces = shlex.split(line.strip())
		    for p in pieces:
			queue.put(p)
			print ("Found: " + p)
			mediaFound = True
		f.close()

		# Only remove the file if we found something in it
		if(mediaFound):
		    os.remove(fpath)
		    print("Deleting file.")

	# Drain events from file operations.
	e = inotifyx.get_events(fd, 0)
	while e:
	    e = inotifyx.get_events(fd, 0)

    inotifyx.rm_watch(fd, wd)
    os.close(fd)

def main():
    queue = Queue.Queue()

    # Start watchFiles() thread
    thread = threading.Thread(target=watchFiles, args=([queue]))
    thread.daemon = True
    thread.start()

    while (1):
	entry = queue.get()
	entryPath = os.path.join(mediaPath, entry)
	print ("Playing: " + entryPath)
	subprocess.call([mediaPlayer, mediaPlayerParams, entryPath])

main()
