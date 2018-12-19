#! /usr/bin/env

all:
	sudo apt-get update
	sudo apt-get install python3
	cp chord /usr/bin/chord
	chmod +x /usr/bin/chord
