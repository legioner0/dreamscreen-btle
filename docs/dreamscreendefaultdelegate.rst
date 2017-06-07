.. _dreamscreendefaultdelegate:

The ``DreamScreenDefaultDelegate`` class
========================================

Example implementaion of ``btle.DefaultDelegate`` class, required for constructor of :ref:`dreamscreen`.

It parse all kinds of notifications from DS with exhaustive correctness check and prints to ``stdout`` content of the notifications in human-readable format.

You should write class derived from ``btle.DefaultDelegate`` and override ``handleNotification`` method with your own application-specific code.

Constructor
-----------

.. function:: DreamScreenDefaultDelegate()

    Initialises the object instance.

Instance Methods
----------------

.. function:: handleNotification(cHandle, data)

   This method will be called on each notification recieved from DS.

   *cHandle* is the (``integer``) handle for the characteristic - in case of DS is only one constant value, not necessary to check.

   **Atention!** DS always send notification with 20 bytes of data. Real data in these 20 bytes - is before ``\r``. Use ``data.split()[0].decode('UTF-8')`` (Python 3.x) for extract data.

   Data looks like ``#<Command name><Command direction><Command data>``, e.g. ``#Br1`` stands for "DS now in Video Mode".
   
   See implementaion of ``DreamScreenDefaultDelegate`` and DS BLE documentation (http://dreamscreen.boards.net/thread/22/dreamscreen-ble-command-set) for more information.
