dreamscreen-btle
================

Python interface to DreamScreen via Bluetooth LE

This is a project to provide an API to control DreamScreen (http://www.dreamscreentv.com/)
via Bluetooth Low Energy from Python. At present it runs on Linux only; 
I've mostly developed it using a Raspberry Pi, but it will also run on x86 Debian Linux.

The code is tested on Python 2.7 and 3.4; it should also work on 3.3.

The code is based on official DreamScreen BLE commands documentation (http://dreamscreen.boards.net/thread/22/dreamscreen-ble-command-set) and answers of 
DreamScreen developers (thanks, Kyle).

Requirements
------------

This module require bluepy and parse packages from pip for work:

	$ sudo pip install bluepy
	$ sudo pip install parse


Demo mode
---------

	$ sudo python dsbtle.py

Will scan for DreamScreen devices and show all avialable information.

Using
-----

	from dsbtle import *
	from bluepy import btle
	
	conn = btle.Peripheral("00:11:22:33:44:55")
	ds = DreamScreen(conn, DreamScreenDefaultDelegate())
	ds.GetMode()
	ds.SetMode(Mode.VIDEO)

Documentation
-------------

Documentation can be built from the sources in the docs/ directory using Sphinx.

TO DO List
----------

- Find new TODO List items
