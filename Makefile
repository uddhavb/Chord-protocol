#! /usr/bin/env

all:
	sudo apt-get update
	sudo apt-get install python3
	chmod +x /usr/bin/chord
	cp chord /usr/bin/chord
