.. dsbtle

``dsbtle`` - a interface to DreamScreen via Bluetooth LE
=========================================================================

``dsbtle`` is a Python module which allows communication with your DreamScreen (DS) devices via Bluetooth Low
Energy. The current implementation runs on Linux, although it can be ported to other platforms.

To browse the API documentation, it is recommended to start with :ref:`dreamscreen`.

DreamScreen communication features, determining architecture of this project
----------------------------------------------------------------------------

DS communication stack is **NOT** designed for frequent requests - you must wait at least 0.1 second between
communication cycles. Ignoring this rule may cause:

* frequently blinking LEDs
* not applied commands
* etc.

Operations sequence for reading data from DS:

* Enable notifitions on response characteristic
* Send read-command to command characteristic, e.g. ``#Br`` for read Mode
* Wait for notification from DS on response characteristic, e.g. ``#Br1`` for Video Mode

Operations sequence for writing data to DS:

* Send write-command to command characteristic, e.g. ``#Bw0`` for Idle Mode

Contents:
---------

.. toctree::
   :maxdepth: 2

   dreamscreen
   dreamscreendefaultdelegate
   command
   commanddirection
   mode
   sku
   customledmode
   musicmodetype
   musicmodecolor
   ambientshowtype
  

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

