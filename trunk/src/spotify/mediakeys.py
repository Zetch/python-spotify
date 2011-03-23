
import dbus

from spotify.settings import \
    DBUS_GNOME_SETTINGS, \
    DBUS_MEDIAKEYS_PATH, \
    DBUS_MEDIAKEYS_IFACE


class KeyHandler(object):

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
