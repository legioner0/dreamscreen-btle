.. _dreamscreen:

The ``DreamScreen`` class
=========================

Dsbtle's ``DreamScreen`` class encapsulates a communications with a DS via Bluetooth LE.

The constructor and all methods will throw a ``AssertionError`` on attributes type mismatch and ``BTLEException`` on communications problems.

Constructor
-----------

.. function:: DreamScreen(connection, delegate)

   *connection* - ``btle.Peripheral`` object.

   *delegate* - reference to a “delegate” object, which is called when asynchronous events such as Bluetooth notifications occur. This must be a subclass of the ``btle.DefaultDelegate`` class, see :ref:`dreamscreendefaultdelegate` for more information.

Instance Methods
----------------

.. function:: EnableNotifications(connection, characteristic)

   Enable notifications on *characteristic*. Called in constructor, by default.

.. function:: WaitForNotifications([timeout=READ_TIMEOUT])

   Wait no more than *timeout* seconds for notifications. 
   
   Call ``btle.Peripheral.waitForNotifications`` method and return it's result - ``True`` if notification is received.

.. function:: SetMode(mode, [timeout=WRITE_TIMEOUT])

   Send command to set *mode* (item of :ref:`mode`). Return self.

.. function:: GetMode([timeout=READ_TIMEOUT])

   Send command to read mode and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetBrightness(brightness, [timeout=WRITE_TIMEOUT])

   Send command to set *brightness* (``integer``, 0..100). Return self.

.. function:: GetBrightness([timeout=READ_TIMEOUT])

   Send command to read brightness and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetZone(top, bottom, left, right, [timeout=WRITE_TIMEOUT])

   Send command to set *zones*. Top, bottom, left, right - bool. Return self.

.. function:: GetZone([timeout=READ_TIMEOUT])

   Send command to read zone status and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetAmbientColor(red, green, blue, [timeout=WRITE_TIMEOUT])

   Send command to set *ambient color*, defined by *red*, *green*, *blue* (``integer``, 0..255). Return self.
   
   **Warning!** Setting ambient color change mode to ``AMBIENT_STATIC`` immediately.

.. function:: GetAmbientColor([timeout=READ_TIMEOUT])

   Send command to read ambient color and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetSaturation(red, green, blue, [timeout=WRITE_TIMEOUT])

   Send command to set *saturation*, defined by *red*, *green*, *blue* (``integer``, 0..255). Return self.

.. function:: GetSaturation([timeout=READ_TIMEOUT])

   Send command to read saturation and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetSKU(sku, [timeout=WRITE_TIMEOUT])

   Send command to set *SKU* (item of :ref:`sku`). Return self.

.. function:: GetSKU([timeout=READ_TIMEOUT])

   Send command to read SKU and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetCustomLEDCount(vertical, horizontal. customLEDMode, [timeout=WRITE_TIMEOUT])

   Send command to set *custom LED count*: vertical (``integer``, 8..32) LEDs count, horizontal (``integer``, 14..60) LEDs count, customLEDMode (item of :ref:`customledmode`). Return self.

.. function:: GetCustomLEDCount([timeout=READ_TIMEOUT])

   Send command to read custom LED count and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetMusicModeType(musicModeType, [timeout=WRITE_TIMEOUT])

   Send command to set *music mode type* (item of :ref:`musicmodetype`). Return self.

   **Warning!** Setting music mode type change mode to ``MUSIC`` immediately.

.. function:: GetMusicModeType([timeout=READ_TIMEOUT])

   Send command to read music mode type and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetMusicModeColor(treble, middle, bass, [timeout=WRITE_TIMEOUT])

   Send command to set *music mode color*, defined by *treble*, *middle*, *bass* (item of :ref:`musicmodecolor`). Return self.

.. function:: GetMusicModeColor([timeout=READ_TIMEOUT])

   Send command to read music mode color and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetVideoMinimumIntensity(red, green, blue, [timeout=WRITE_TIMEOUT])

   Send command to set *video minimum intensity*, defined by *red*, *green*, *blue* (``integer``, 0..50). Return self.

.. function:: GetVideoMinimumIntensity([timeout=READ_TIMEOUT])

   Send command to read video minimum intensity and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetAmbientShowType(ambientShowType, [timeout=WRITE_TIMEOUT])

   Send command to set *ambient show type* (item of :ref:`ambientshowtype`). Return self.

   **Warning!** Setting ambient show type change mode to ``AMBIENT_SHOW`` immediately.

.. function:: GetAmbientShowType([timeout=READ_TIMEOUT])

   Send command to read ambient show type and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetFadeRate(fadeRate, [timeout=WRITE_TIMEOUT])

   Send command to set *fade rate* (``integer``, 4..50). Return self.

.. function:: GetFadeRate([timeout=READ_TIMEOUT])

   Send command to read fade rate and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: GetVersionNumber([timeout=READ_TIMEOUT])

   Send command to read firmware version number and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetMusicModeWeights(treble, middle, bass, [timeout=WRITE_TIMEOUT])

   Send command to set *music mode weights*, defined by *treble*, *middle*, *bass* (``integer``, 5..25). Return self.

.. function:: GetMusicModeWeights([timeout=READ_TIMEOUT])

   Send command to read music mode weights and wait for notification. Return result of *WaitForNotifications(timeout)* call.

.. function:: SetName(name)

   Set device *name* (``str``). Return self.

.. function:: GetName()

   Read device *name* and return it in ``str``.
