#!/usr/bin/env python

''' DreamScreen interface via BLE '''
import sys
from enum import Enum
from bluepy import btle
from parse import *

Debugging = False
def DBG(*args):
    if Debugging:
        msg = " ".join([str(a) for a in args])
        print(msg)

COMMAND_CHAR = '#'
WRITE_TIMEOUT = 0.1
READ_TIMEOUT = 1.0

class Command(Enum):
	'''DreamScreen Commands'''
	MODE = 'B'
	BRIGHTNESS = 'C'
	ZONE = 'D'
	AMBIENT_COLOR = 'E'
	SATURATION = 'F'
	SKU = 'G'
	CUSTOM_LED_COUNT = 'H'
	MUSIC_MODE_TYPE = 'J'
	MUSIC_MODE_COLOR = 'K'
	VIDEO_MINIMUM_INTENSITY = 'L'
	AMBIENT_SHOW_TYPE = 'M'
	FADE_RATE = 'N'
	VERSION_NUMBER = 'O'
	MUSIC_MODE_WEIGHTS = 'P'

class CommandDirection(Enum):
	'''DreamScreen command direction'''
	READ = 'r'
	WRITE = 'w'
	USER = 'u'

class Mode(Enum):
	'''DreamScreen Modes'''
	IDLE = 0
	VIDEO = 1
	MUSIC = 2
	AMBIENT_STATIC = 3
	IDENTIFY = 4	# This mode lights blue for a few seconds and returns to the previous mode
	AMBIENT_SHOW = 5

class SKU(Enum):
	'''DreamScreen SKU'''
	CLASSIC = 0
	MEGA = 1
	XTREME = 2
	CUSTOM = 3

class CustomLEDMode(Enum):
	'''DreamScreen starting point and rotation of how the LEDs are installed, referenced from the front of the TV, for custom SKU'''
	RIGHT_COUNTER_CLOCKWISE = 'a'
	TOP_COUNTER_CLOCKWISE = 'b'
	LEFT_COUNTER_CLOCKWISE = 'c'
	BOTTOM_COUNTER_CLOCKWISE = 'd'
	RIGHT_CLOCKWISE = 'e'
	TOP_CLOCKWISE = 'f'
	LEFT_CLOCKWISE = 'g'
	BOTTOM_CLOCKWISE = 'h'

class MusicModeType(Enum):
	'''DreamScreen music type mode'''
	TOP_N_BOTTOM_TO_MIDDLE = 0
	MIDDLE_TO_TOP_N_BOTTOM = 1
	BOTTOM_CORNERS_TO_TOP = 2
	BOTTOM_TO_TOP = 3

class MusicModeColor(Enum):
	'''DreamScreen music mode color'''
	RED = 0
	GREEN = 1
	BLUE = 2

class AmbientShowType(Enum):
	'''DreamScreen ambient show type'''
	COLORS = 0
	FIRE = 1
	TWINKLE = 2
	OCEAN = 3
	RAINBOW = 4
	JULY_4TH = 5
	HOLIDAY = 6
	POP = 7
	ENCHANTED_FOREST = 8

class DreamScreenDefaultDelegate(btle.DefaultDelegate):
	def __init__(self):
		btle.DefaultDelegate.__init__(self)

	def handleNotification(self, cHandle, data):
		response = data.split()[0].decode('UTF-8')
		DBG('%s %s' % (hex(cHandle), response), 'WHITE')
		assert (len(response) > 3), 'response length must be greather than 3: %r (%d)' % (response, len(response))
		assert (response[0] == COMMAND_CHAR), 'response must start with %s: %r' % (COMMAND_CHAR, response[0])

		try:
			command = Command(response[1])
		except ValueError as e:
			assert False, 'command is not recognised: %r' % response[1]

		try:
			commandDirection = CommandDirection(response[2])
		except ValueError as e:
			assert False, 'command direction is not recognised: %r' % response[2]
		assert (commandDirection != CommandDirection.WRITE), 'command direction - write! Impossibru!'

		argument = response[3:]

		out = "User pressed buttons. Now " if (commandDirection == CommandDirection.USER) else "Response: "
		out += "%s is " % command.name
		if command == Command.MODE:
			try:
				out += "%s" % Mode(parse('{:d}', argument)[0]).name
			except ValueError as e:
				assert False, 'mode is not recognised: %r' % argument
		elif command == Command.BRIGHTNESS:
			brightness = parse('{:d}', argument)[0]
			assert (isinstance(brightness, int) and (brightness >= 0) and (brightness <= 100)), 'brightness must be int between 0 and 100: %r' % brightness
			out += "%d/100" % brightness
		elif command == Command.ZONE:
			top = (argument[0] == 'y')
			bottom = (argument[1] == 'y')
			left = (argument[2] == 'y')
			right = (argument[3] == 'y')
			out += 'top: %s, bottom: %s, left: %s, right: %s' % ("on" if top else "off", "on" if bottom else "off", "on" if left else "off", "on" if right else "off")
		elif command == Command.AMBIENT_COLOR:
			red = parse('{:d}', argument[0:3])[0]
			green = parse('{:d}', argument[3:6])[0]
			blue = parse('{:d}', argument[6:])[0]
			assert (isinstance(red, int) and (red >= 0) and (red <= 255)), 'red must be int between 0 and 255: %r' % red
			assert (isinstance(green, int) and (green >= 0) and (green <= 255)), 'green must be int between 0 and 255: %r' % green
			assert (isinstance(blue, int) and (blue >= 0) and (blue <= 255)), 'blue must be int between 0 and 255: %r' % blue
			out += 'red: %d/255, green: %d/255, blue: %d/255' % (red, green, blue)
		elif command == Command.SATURATION:
			red = parse('{:d}', argument[0:3])[0]
			green = parse('{:d}', argument[3:6])[0]
			blue = parse('{:d}', argument[6:])[0]
			assert (isinstance(red, int) and (red >= 0) and (red <= 255)), 'red must be int between 0 and 255: %r' % red
			assert (isinstance(green, int) and (green >= 0) and (green <= 255)), 'green must be int between 0 and 255: %r' % green
			assert (isinstance(blue, int) and (blue >= 0) and (blue <= 255)), 'blue must be int between 0 and 255: %r' % blue
			out += 'red: %d/255, green: %d/255, blue: %d/255' % (red, green, blue)
		if command == Command.SKU:
			try:
				out += "%s" % SKU(parse('{:d}', argument)[0]).name
			except ValueError as e:
				assert False, 'SKU is not recognised: %r' % argument
		elif command == Command.CUSTOM_LED_COUNT:
			vertical = parse('{:d}', argument[0:3])[0]
			horizontal = parse('{:d}', argument[3:6])[0]
			try:
				customLEDMode = CustomLEDMode(argument[6])
			except ValueError as e:
				assert False, 'customLEDMode is not recognised: %r' % argument
			assert (isinstance(vertical, int) and (vertical >= 8) and (vertical <= 32)), 'vertical must be int between 8 and 32: %r' % vertical
			assert (isinstance(horizontal, int) and (horizontal >= 14) and (horizontal <= 60)), 'horizontal must be int between 14 and 60: %r' % horizontal
			out += 'vertical: %d LEDs (min 8, max 32), horizontal: %d LEDs (min 14, max 60), %s' % (vertical, horizontal, customLEDMode.name)
		if command == Command.MUSIC_MODE_TYPE:
			try:
				out += "%s" % MusicModeType(parse('{:d}', argument)[0]).name
			except ValueError as e:
				assert False, 'MusicModeType is not recognised: %r' % argument
		if command == Command.MUSIC_MODE_COLOR:
			try:
				out += 'treble: %s, ' % MusicModeColor(parse('{:d}', argument[0])[0]).name
			except ValueError as e:
				assert False, 'MusicModeColor is not recognised: %r' % argument[0]
			try:
				out += 'middle: %s, ' % MusicModeColor(parse('{:d}', argument[1])[0]).name
			except ValueError as e:
				assert False, 'MusicModeColor is not recognised: %r' % argument[1]
			try:
				out += 'bass: %s' % MusicModeColor(parse('{:d}', argument[2])[0]).name
			except ValueError as e:
				assert False, 'MusicModeColor is not recognised: %r' % argument[2]
		elif command == Command.VIDEO_MINIMUM_INTENSITY:
			red = parse('{:d}', argument[0:3])[0]
			green = parse('{:d}', argument[3:6])[0]
			blue = parse('{:d}', argument[6:])[0]
			assert (isinstance(red, int) and (red >= 0) and (red <= 50)), 'red must be int between 0 and 50: %r' % red
			assert (isinstance(green, int) and (green >= 0) and (green <= 50)), 'green must be int between 0 and 50: %r' % green
			assert (isinstance(blue, int) and (blue >= 0) and (blue <= 50)), 'blue must be int between 0 and 50: %r' % blue
			out += 'red: %d/50, green: %d/50, blue: %d/50' % (red, green, blue)
		if command == Command.AMBIENT_SHOW_TYPE:
			try:
				out += "%s" % AmbientShowType(parse('{:d}', argument)[0]).name
			except ValueError as e:
				assert False, 'AmbientShowType is not recognised: %r' % argument
		elif command == Command.FADE_RATE:
			fateRate = parse('{:d}', argument)[0]
			assert (isinstance(fateRate, int) and (fateRate >= 4) and (fateRate <= 50)), 'fateRate must be int between 4 and 50: %r' % fateRate
			out += "%d (min 4, max 50)" % fateRate
		elif command == Command.VERSION_NUMBER:
			major = parse('{:d}', argument[0:2])[0]
			minor = parse('{:d}', argument[2:4])[0]
			assert (isinstance(major, int) and (major >= 0) and (major <= 99)), 'major must be int between 0 and 99: %r' % major
			assert (isinstance(minor, int) and (minor >= 0) and (minor <= 99)), 'minor must be int between 0 and 99: %r' % minor
			out += '%d.%d' % (major, minor)
		elif command == Command.MUSIC_MODE_WEIGHTS:
			treble = parse('{:d}', argument[0:3])[0]
			middle = parse('{:d}', argument[3:6])[0]
			bass = parse('{:d}', argument[6:])[0]
			assert (isinstance(treble, int) and (treble >= 5) and (treble <= 25)), 'treble must be int between 5 and 25: %r' % treble
			assert (isinstance(middle, int) and (middle >= 5) and (middle <= 25)), 'middle must be int between 5 and 25: %r' % middle
			assert (isinstance(bass, int) and (bass >= 5) and (bass <= 25)), 'bass must be int between 5 and 25: %r' % bass
			out += 'treble: %d, middle: %d, bass: %d (min 5, max 25)' % (treble, middle, bass)
			
		print(out)

class DreamScreen:
	def __init__(self, connection, peripheralDelegate):
		assert isinstance(connection, btle.Peripheral), 'connection must be btle.Peripheral'
		assert isinstance(peripheralDelegate, btle.DefaultDelegate), 'peripheralDelegate must be btle.DefaultDelegate'
		DBG('__init__')
		self.connection = connection
		self.connection.setDelegate(peripheralDelegate)

		self.ds_service = connection.getServiceByUUID('0000ff60-0000-1000-8000-00805f9b34fb')
		self.ds_command_char = self.ds_service.getCharacteristics('0000ff61-0000-1000-8000-00805f9b34fb')[0]
		self.ds_response_char = self.ds_service.getCharacteristics('0000ff62-0000-1000-8000-00805f9b34fb')[0]
		self.ds_name_char = self.ds_service.getCharacteristics('0000ff63-0000-1000-8000-00805f9b34fb')[0]

		self.EnableNotifications(self.connection, self.ds_response_char)

	def __del__(self):
		pass

	def EnableNotifications(self, connection, characteristic):
		DBG('EnableNotifications')
		assert isinstance(connection, btle.Peripheral), 'connection must be btle.Peripheral'
		assert isinstance(characteristic, btle.Characteristic), 'characteristic must be btle.Characteristic'
		for d in connection.getDescriptors(characteristic.getHandle(), characteristic.getHandle() + 1):
			if (d.uuid == btle.AssignedNumbers.client_characteristic_configuration):
				connection.writeCharacteristic(d.handle, b'\1\0')
				return True
		return False

	def WaitForNotifications(self, timeout=READ_TIMEOUT):
		return self.connection.waitForNotifications(timeout)
		
	def _transmitCommand(self, command, direction=CommandDirection.READ, argument=''):
		assert isinstance(command, Command), 'command must be Commands: %r' % command
		assert isinstance(direction, CommandDirection), 'direction must be CommandDirection: %r' % direction
		assert isinstance(argument, str), 'argument must be string: %r' % argument
		DBG('_transmitCommand(%s, %s, %s)' % (command.value, direction.value, argument))
		self.ds_command_char.write(('%s%s%s%s' % (COMMAND_CHAR, command.value, direction.value, argument)).encode('UTF-8'))
		return self

	def _writeCommandNWait(self, command, argument, timeout=WRITE_TIMEOUT):
		DBG('_writeCommandNWait(%s)' % command.value)
		self._transmitCommand(command, CommandDirection.WRITE, argument).WaitForNotifications(timeout)
		return self

	def _readCommandNWait(self, command, timeout=READ_TIMEOUT):
		DBG('_readCommandNWait(%s)' % command.value)
		return self._transmitCommand(command, CommandDirection.READ).WaitForNotifications(timeout)

	def SetMode(self, mode, timeout=WRITE_TIMEOUT):
		assert isinstance(mode, Mode), 'mode must be Mode: %r' % mode
		DBG('SetMode(%d)' % mode.value)
		return self._writeCommandNWait(Command.MODE, '%d' % mode.value, timeout)

	def GetMode(self, timeout=READ_TIMEOUT):
		DBG('GetMode')
		return self._readCommandNWait(Command.MODE, timeout)
		
	def SetBrightness(self, brightness, timeout=WRITE_TIMEOUT):
		assert (isinstance(brightness, int) and (brightness >= 0) and (brightness <= 100)), 'brightness must be int between 0 and 100: %r' % brightness
		DBG('SetBrightness(%d)' % brightness)
		return self._writeCommandNWait(Command.BRIGHTNESS, '%03d' % brightness, timeout)

	def GetBrightness(self, timeout=READ_TIMEOUT):
		DBG('GetBrightness')
		return self._readCommandNWait(Command.BRIGHTNESS, timeout)
		
	def SetZone(self, top, bottom, left, right, timeout=WRITE_TIMEOUT):
		assert isinstance(top, bool), 'top must be bool: %r' % top
		assert isinstance(bottom, bool), 'bottom must be bool: %r' % bottom
		assert isinstance(left, bool), 'left must be bool: %r' % left
		assert isinstance(right, bool), 'right must be bool: %r' % right
		DBG('SetZone(%s, %s, %s, %s)' % (top, bottom, left, right))
		return self._writeCommandNWait(Command.ZONE, ('y' if top else 'n') + ('y' if bottom else 'n') + ('y' if left else 'n') + ('y' if right else 'n'))

	def GetZone(self, timeout=READ_TIMEOUT):
		DBG('GetZone')
		return self._readCommandNWait(Command.ZONE, timeout)
		
	def SetAmblientColor(self, red, green, blue, timeout=WRITE_TIMEOUT):
		assert (isinstance(red, int) and (red >= 0) and (red <= 255)), 'red must be int between 0 and 255: %r' % red
		assert (isinstance(green, int) and (green >= 0) and (green <= 255)), 'green must be int between 0 and 255: %r' % green
		assert (isinstance(blue, int) and (blue >= 0) and (blue <= 255)), 'blue must be int between 0 and 255: %r' % blue
		DBG('SetAmblientColor(%d, %d, %d)' % (red, green, blue))
		return self._writeCommandNWait(Command.AMBIENT_COLOR, '%03d%03d%03d' % (red, green, blue), timeout)

	def GetAmblientColor(self, timeout=READ_TIMEOUT):
		DBG('GetAmblientColor')
		return self._readCommandNWait(Command.AMBIENT_COLOR, timeout)
		
	def SetSaturation(self, red, green, blue, timeout=WRITE_TIMEOUT):
		assert (isinstance(red, int) and (red >= 0) and (red <= 255)), 'red must be int between 0 and 255: %r' % red
		assert (isinstance(green, int) and (green >= 0) and (green <= 255)), 'green must be int between 0 and 255: %r' % green
		assert (isinstance(blue, int) and (blue >= 0) and (blue <= 255)), 'blue must be int between 0 and 255: %r' % blue
		DBG('SetSaturation(%d, %d, %d)' % (red, green, blue))
		return self._writeCommandNWait(Command.SATURATION, '%03d%03d%03d' % (red, green, blue), timeout)

	def GetSaturation(self, timeout=READ_TIMEOUT):
		DBG('GetSaturation')
		return self._readCommandNWait(Command.SATURATION, timeout)
		
	def SetSKU(self, sku, timeout=WRITE_TIMEOUT):
		assert isinstance(sku, SKU), 'sku must be SKU: %r' % sku
		DBG('SetSKU(%d)' % sku.value)
		return self._writeCommandNWait(Command.SKU, '%d' % sku.value, timeout)

	def GetSKU(self, timeout=READ_TIMEOUT):
		DBG('GetSKU')
		return self._readCommandNWait(Command.SKU, timeout)
		
	def SetCustomLEDCount(self, vertical, horizontal, customLEDMode, timeout=WRITE_TIMEOUT):
		assert (isinstance(vertical, int) and (vertical >= 8) and (vertical <= 32)), 'vertical must be int between 8 and 32: %r' % vertical
		assert (isinstance(horizontal, int) and (horizontal >= 14) and (horizontal <= 60)), 'horizontal must be int between 14 and 60: %r' % horizontal
		assert isinstance(customLEDMode, CustomLEDMode), 'customLEDMode must be CustomLEDMode: %r' % customLEDMode
		DBG('SetCustomLEDCount(%d, %d, %s)' % (vertical, horizontal, customLEDMode.value))
		return self._writeCommandNWait(Command.CUSTOM_LED_COUNT, '%03d%03d%s' % (vertical, horizontal, customLEDMode.value), timeout)

	def GetCustomLEDCount(self, timeout=READ_TIMEOUT):
		DBG('GetCustomLEDCount')
		return self._readCommandNWait(Command.CUSTOM_LED_COUNT, timeout)
		
	def SetMusicModeType(self, musicModeType, timeout=WRITE_TIMEOUT):
		assert isinstance(musicModeType, MusicModeType), 'musicModeType must be MusicModeType: %r' % musicModeType
		DBG('SetMusicModeType(%d)' % musicModeType.value)
		return self._writeCommandNWait(Command.MUSIC_MODE_TYPE, '%d' % musicModeType.value, timeout)

	def GetMusicModeType(self, timeout=READ_TIMEOUT):
		DBG('GetMusicModeType')
		return self._readCommandNWait(Command.MUSIC_MODE_TYPE, timeout)
		
	def SetMusicModeColor(self, treble, middle, bass, timeout=WRITE_TIMEOUT):
		assert isinstance(treble, MusicModeColor), 'treble must be MusicModeColor: %r' % treble
		assert isinstance(middle, MusicModeColor), 'middle must be MusicModeColor: %r' % middle
		assert isinstance(bass, MusicModeColor), 'bass must be MusicModeColor: %r' % bass
		DBG('SetMusicModeColor(%d, %d, %d)' % (treble.value, middle.value, bass.value))
		return self._writeCommandNWait(Command.MUSIC_MODE_COLOR, '%d%d%d' % (treble.value, middle.value, bass.value), timeout)

	def GetMusicModeColor(self, timeout=READ_TIMEOUT):
		DBG('GetMusicModeColor')
		return self._readCommandNWait(Command.MUSIC_MODE_COLOR, timeout)
		
	def SetVideoMinimumIntensity(self, red, green, blue, timeout=WRITE_TIMEOUT):
		assert (isinstance(red, int) and (red >= 0) and (red <= 50)), 'red must be int between 0 and 50: %r' % red
		assert (isinstance(green, int) and (green >= 0) and (green <= 50)), 'green must be int between 0 and 50: %r' % green
		assert (isinstance(blue, int) and (blue >= 0) and (blue <= 50)), 'blue must be int between 0 and 50: %r' % blue
		DBG('SetVideoMinimumIntensity(%d, %d, %d)' % (red, green, blue))
		return self._writeCommandNWait(Command.VIDEO_MINIMUM_INTENSITY, '%03d%03d%03d' % (red, green, blue), timeout)

	def GetVideoMinimumIntensity(self, timeout=READ_TIMEOUT):
		DBG('GetVideoMinimumIntensity')
		return self._readCommandNWait(Command.VIDEO_MINIMUM_INTENSITY, timeout)
		
	def SetAmbientShowType(self, ambientShowType, timeout=WRITE_TIMEOUT):
		assert isinstance(ambientShowType, AmbientShowType), 'ambientShowType must be AmbientShowType: %r' % ambientShowType
		DBG('SetAmbientShowType(%d)' % ambientShowType.value)
		return self._writeCommandNWait(Command.AMBIENT_SHOW_TYPE, '%d' % ambientShowType.value, timeout)

	def GetAmbientShowType(self, timeout=READ_TIMEOUT):
		DBG('GetAmbientShowType')
		return self._readCommandNWait(Command.AMBIENT_SHOW_TYPE, timeout)
		
	def SetFadeRate(self, fadeRate, timeout=WRITE_TIMEOUT):
		assert (isinstance(fadeRate, int) and (fadeRate >= 4) and (fadeRate <= 50)), 'fadeRate must be int between 4 and 50: %r' % fadeRate
		DBG('SetFadeRate(%d)' % fadeRate)
		return self._writeCommandNWait(Command.FADE_RATE, '%03d' % fadeRate, timeout)

	def GetFadeRate(self, timeout=READ_TIMEOUT):
		DBG('GetFadeRate')
		return self._readCommandNWait(Command.FADE_RATE, timeout)
		
	def GetVersionNumber(self, timeout=READ_TIMEOUT):
		DBG('GetVersionNumber')
		return self._readCommandNWait(Command.VERSION_NUMBER, timeout)
		
	def SetMusicModeWeights(self, treble, middle, bass, timeout=WRITE_TIMEOUT):
		assert (isinstance(treble, int) and (treble >= 5) and (treble <= 25)), 'treble must be int between 5 and 25: %r' % treble
		assert (isinstance(middle, int) and (middle >= 5) and (middle <= 25)), 'middle must be int between 5 and 25: %r' % middle
		assert (isinstance(bass, int) and (bass >= 5) and (bass <= 25)), 'bass must be int between 5 and 25: %r' % bass
		DBG('SetMusicModeWeights(%d, %d, %d)' % (treble, middle, bass))
		return self._writeCommandNWait(Command.MUSIC_MODE_WEIGHTS, '%03d%03d%03d' % (treble, middle, bass), timeout)

	def GetMusicModeWeights(self, timeout=READ_TIMEOUT):
		DBG('GetMusicModeWeights')
		return self._readCommandNWait(Command.MUSIC_MODE_WEIGHTS, timeout)
		
	def SetName(self, name):
		assert isinstance(name, str), 'name must be string: %r' % name
		DBG('SetName(%s)' % name)
		return self.ds_name_char.write(('%s' % name).encode('UTF-8'))

	def GetName(self):
		DBG('GetName')
		return self.ds_name_char.read()

if __name__ == '__main__':
	try:
		print('[!] Scan')
		conn = None
		try:
			devices = btle.Scanner().scan(1.0)
		except btle.BTLEException as e:
			sys.exit('Whoa1!!1 %s' % e.message)
		print('Found %d devices' % len(devices))

		for dev in devices:
			print('Device %s (%s), RSSI=%d dB' % (dev.addr, dev.addrType, dev.rssi))
			try:
				if not dev.connectable:
					print('[!] This device is not connectable. Skipping')
					continue
			
				conn = btle.Peripheral(dev.addr)
				name = conn.getServiceByUUID(btle.AssignedNumbers.generic_access).getCharacteristics(btle.AssignedNumbers.deviceName)[0].read().decode('UTF-8')
				if (name != 'DreamScreen'):
					conn.disconnect()
					print('[!] This is not DreamScreen (%s). Skipping' % name)
					continue

				print('DreamScreen connect success')

				ds = DreamScreen(conn, DreamScreenDefaultDelegate())

				print('DreamScreen name: %s' % ds.GetName().decode('UTF-8'))
			
				ds.GetMode()
				ds.SetMode(Mode.IDENTIFY)
				ds.GetBrightness()
				ds.GetZone()
				ds.GetAmblientColor()
				ds.GetSaturation()
				ds.GetSKU()
				ds.GetCustomLEDCount()
				ds.GetMusicModeType()
				ds.GetMusicModeColor()
				ds.GetVideoMinimumIntensity()
				ds.GetAmbientShowType()
				ds.GetFadeRate()
				ds.GetVersionNumber()
				ds.GetMusicModeWeights()

				conn.disconnect()
			except btle.BTLEException as e:
				assert (e.code == btle.BTLEException.DISCONNECTED), e.message
				print('Whoa1!!1 %s' % e.message)
				continue
	except AssertionError as e:
		print('Whoa1!!1 %s' % e)
	except KeyboardInterrupt:
		print('Stop')
	finally:
		if conn:
			conn.disconnect()
