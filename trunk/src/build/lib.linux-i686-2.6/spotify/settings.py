
# *************************************************************************** #
# Settings file
# *************************************************************************** #

import os.path


# D-Bus Settings

DBUS_SPOTIFY_BUS          = 'com.spotify.qt'
DBUS_PROPERTY_IFACE       = 'org.freedesktop.DBus.Properties'
DBUS_MEDIAPLAYER_IFACE    = 'org.freedesktop.MediaPlayer2'

DBUS_NOTIFICATION_BUS     = 'org.freedesktop.Notifications'
DBUS_NOTIFICATION_IFACE   = 'org.freedesktop.Notifications'
DBUS_NOTIFICATION_PATH    = '/org/freedesktop/Notifications'

DBUS_GNOME_SETTINGS       = ''
DBUS_MEDIAKEYS_PATH       = ''
DBUS_MEDIAKEYS_IFACE      = ''


# Path settings

DEFAULT_SPOTIFY_ICON      = '/usr/share/pixmaps/spotify.png'
CACHE_DIR                 = os.path.join(os.environ['HOME'], '.cache/spotify/Covers/')