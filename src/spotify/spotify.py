# *********************************************************************** #
# Spotify Python API
# Author: Nauzet Hernandez (nauzethc@gmail.com)
# *********************************************************************** #


import dbus
import urllib2
import os
import hashlib

from gobject import MainLoop
from dbus.mainloop.glib import DBusGMainLoop
from re import compile

DBUS_SPOTIFY_BUS = 'com.spotify.qt'
DBUS_PROPERTY_IFACE = 'org.freedesktop.DBus.Properties'
DBUS_MEDIAPLAYER_IFACE = 'org.freedesktop.MediaPlayer2'
DBUS_NOTIFICATION_BUS = 'org.freedesktop.Notifications'
DBUS_NOTIFICATION_IFACE = 'org.freedesktop.Notifications'
DBUS_NOTIFICATION_PATH = '/org/freedesktop/Notifications'
DBUS_GNOME_SETTINGS = ''
DBUS_MEDIAKEYS_PATH = ''

DEFAULT_SPOTIFY_ICON = '/usr/share/pixmaps/spotify.png'
CACHE_DIR = os.path.join(os.environ['HOME'], '.cache/spotify/Covers/')


class SpotifyHandler(object):

	def __init__(self, bus=dbus.SessionBus()):
		try:
			self.__bus  = bus.get_object(DBUS_SPOTIFY_BUS, '/')
			self.player = dbus.Interface(self.__bus, DBUS_MEDIAPLAYER_IFACE)
			self.bridge = dbus.Interface(self.__bus, DBUS_PROPERTY_IFACE)
		except Exception:
			print "Spotify not running!"
		# Patterns for finding image urls on html
		self.__cover_pattern = compile("""<img class\=\"limit\-width\" src\=\"(.*)\" alt""")
		self.__thumb_pattern = compile("<meta property=\"og\:image\" content\=\"(.*)\" \/>")

	def __catch_except(function):
		'''
		Decorator for catching exception in common MPRIS2 methods
		Returns a status due to right execution of below methods
		'''
		def inner(*args, **kwargs):
			try:
				# Returns 'True' if function executes without errors
				function(*args, **kwargs)
				return True
			except:
				return False
		return inner

	def __omit_optparse(function):
		'''
		Decorator to omit optional args in callback action if method
		is called from OptionParser object
		'''
		def inner(*args, **kwargs):
			function(args[0])
		return inner

	def __filter_optparse(function):
		'''
		Decorator to filter optional args in callback action if method
		is called from OptionParser object, and print to STDOUT
		'''
		def inner(*args, **kwargs):
			if len(args) > 2:
				print function(args[0], args[3])
			else:
				return function(args[0], args[1])
		return inner

	# Common methods due to MPRIS2 specifications
	@__catch_except
	@__omit_optparse
	def next(self): self.player.Next()
	@__catch_except
	@__omit_optparse
	def previous(self):	self.player.Previous()
	@__catch_except
	@__omit_optparse
	def pause(self): self.player.Pause()
	@__catch_except
	@__omit_optparse
	def play_pause(self): self.player.PlayPause()
	@__catch_except
	@__omit_optparse
	def stop(self): self.player.Stop()
	@__catch_except
	@__omit_optparse
	def play(self): self.player.Play()
	@__catch_except
	@__omit_optparse
	def seek(self, offset): self.player.Seek(offset)
	@__catch_except
	@__omit_optparse
	def set_position(self, track, position): self.Player.SetPosition(track, position)
	@__catch_except
	@__omit_optparse
	def open_uri(self, uri): self.Player.OpenUri(uri)

	@__filter_optparse
	def get_property(self, property_name):
		'''
		Getter method
		Common properties due to MPRIS2 specifications
		'''
		valid_properties = (
			'PlaybackStatus', 'LoopStatus',
			'Rate',           'Shuffle',
			'Metadata',       'Identity',
			'Position',       'MinimumRate',
			'MaximumRate',    'CanGoNext',
			'CanGoPrevious',  'CanPlay',
			'CanPause',       'CanSeek',
			'CanControl',     'CanQuit',
			'CanRaise',       'SupportedUriSchemes',
			'DesktopEntry',   'SupportedMimeTypes',
			'HasTrackList', )
		if property_name in valid_properties:
			return self.bridge.Get(DBUS_MEDIAPLAYER_IFACE, property_name)
		elif property_name == 'Volume':
			return self.player.Volume()
		else:
			excep = Exception()
			excep.message = "'%s' is not a valid property name"
			raise excep
		return None

	def set_property(self, property_name, value):
		'''
		Setter method
		Common properties due to MPRIS2 specifications
		'''
		valid_properties = {
			'Volume':   self.player.SetVolume,
			'Rate':     self.player.SetRate,
			'Shuffle':  self.player.SetShuffle,
			'Position': self.player.SetPosition, }
		if property_name in valid_properties.keys():
			valid_properties[property_name](value)
			return True
		else:
			excep = Exception()
			excep.message = "'%s' is not a valid property name"
			raise excep
		return False

	@__filter_optparse
	def get_meta(self, meta):
		'''
		Returns given meta-name value from current playing track
		It uses more user-friendly names for input 'meta' param
		'''
		metadata = {
			'title':    'xesam:title',
			'artist':   'xesam:artist',
			'album':    'xesam:album',
			'track':    'xesam:trackNumber',
			'uri':      'xesam:url',
			'created':  'xesam:contentCreated',
			'disc':     'xesam:discNumber',
			'length':   'mpris:length',
			'trackid':  'mpris:trackid', }

		# Get common metadata
		if meta in metadata.keys():
			try:
				return self.player.GetMetadata().get(metadata[meta])
			except Exception, e:
				print "There was an error:", e

		# Get formatted length 'M:SS'
		elif meta == 'formatlength':
			secs = int(self.get_meta('length')) / 1000000
			flength = "%d:%02d" % (secs/60, secs%60)
			return flength
		
		# Get track Spotify URL
		elif meta == 'url':
			try:
				return 'http://open.spotify.com/track/' + \
					   self.get_meta('trackid').split(':')[2]
			except Exception, e:
				print "Track url not available:", e

		# Get cover image URL
		elif meta == 'coverurl':
			url = self.get_meta('url')
			if url:
				html = urllib2.urlopen(url).read()
				match_image = self.__cover_pattern.search(html)
				if match_image:
					return match_image.groups()[0]
				#
			#
		# Get cover image thumb URL
		elif meta == 'coverurl_thumb':
			url = self.get_meta('url')
			if url:
				html = urllib2.urlopen(url).read()
				match_image = self.__thumb_pattern.search(html)
				if match_image:
					return match_image.groups()[0]
				#
			#
		return None

	@__filter_optparse
	def fetch_cover(self, artist=None, album=None, thumb=True):
		'''
		Fetch current song cover from Spotify web
		Returns a path to cover file if it could reach it,
		otherwise returns default icon path
		'''
		# If no given data, get from current song
		if (not artist) and (not album):
			artist = self.get_meta('artist')
			album  = self.get_meta('album')
		# Checks that cache dir exists
		if not os.path.isdir(CACHE_DIR):
			os.makedirs(CACHE_DIR)
		# Generates a hash for cover filename
		hasher = hashlib.new('md5')
		if thumb:
			hasher.update( self.get_meta('artist') + self.get_meta('album') )
			coverurl = self.get_meta('coverurl_thumb')
		else:
			hasher.update( self.get_meta('artist') + self.get_meta('album') + 'thumb' )
			coverurl = self.get_meta('coverurl')
		filename = hasher.hexdigest()
		filename = os.path.join(CACHE_DIR, filename)
		# Check that cover is not already cached
		if not os.path.isfile( os.path.join(CACHE_DIR, filename) ):
			# Get cover url for writing to disk
			if coverurl:
				try:
					# Write cover image data to file
					coverdata = urllib2.urlopen(coverurl).read()
					coverfile = open(filename, 'wb')
					coverfile.write(coverdata)
					coverfile.close()
					return filename
				except Exception, e:
					print "Couldn't get URL image from web...", e
			return DEFAULT_SPOTIFY_ICON
		return filename


class SpotifyListener(object):

	def __init__(self):
		# TODO
		'''
		bus_loop     = DBusGMainLoop(set_as_default = True)
		bus          = dbus.SessionBus(mainloop = bus_loop)
		self.__loop  = MainLoop()
		spotify_loop = bus.get_object(DBUS_SPOTIFY_BUS, "/")

		# Connect functions to signals
		spotify_loop.connect_to_signal("TrackChange", self.on_track_changed)

		# Start Loop
		self.__loop.run()
		'''
		pass

	def on_track_changed(self):
		pass


class SpotifyNotifier(object):

	def __init__(self, bus=dbus.SessionBus()):
		try:
			self.__bus = bus.get_object(DBUS_NOTIFICATION_BUS, DBUS_NOTIFICATION_PATH)
			self.notifier = dbus.Interface(self.__bus, DBUS_NOTIFICATION_IFACE)
		except Exception, e:
			print "Notification Daemon not running!"

	def notify(self, title, body, timeout, icon=DEFAULT_SPOTIFY_ICON):
		'''
		Displays a notification with given args:
			title: Bold type title
			body: A description text, accepts new-line character
			timeout: Time to display notification
			icon: Path to icon file
		'''
		app_name = "Spotify Notification"
		notification_id = 0
		actions = ()
		hints = {}
		try:
			return self.notifier.Notify(app_name, notification_id, icon, title, body, actions, hints, timeout)
		except Exception, e:
			print "There was an error: ", e
		return 0

	def close_notification(self, notification_id):
		'''
		Close given ID notification if it is displaying
		'''
		try:
			self.notifier.Close(notification_id)
			return True
		except:
			pass
		return False


class MediaKeyHandler(object):

	def __init__(self, spotify_handler, bus=dbus.SessionBus()):
		self.spotify = spotify_handler
		self.__bus   = bus
		self.handler = self.__bus.get_object(DBUS_GNOME_SETTINGS, DBUS_MEDIAKEYS_PATH)
		self.handler.GrabMediaPlayerKeys("Spotify", 0, dbus_interface=DBUS_MEDIAKEYS_IFACE)
		self.handler.connect_to_signal('MediaPlayerKeyPressed', self.on_pressed_key)

	def on_pressed_key(self, *keys):
		for key in keys:
			if key == 'Play': self.spotify.play()
			elif key == 'Stop': self.spotify.stop()
			elif key == 'Next': self.spotify.next()
			elif key == 'Previous': self.spotify.previous()
			elif key == 'Pause': self.spotify.play_pause()
		#
