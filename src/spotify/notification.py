
import dbus

from spotify.settings import \
    DBUS_NOTIFICATION_BUS, \
    DBUS_NOTIFICATION_PATH, \
    DBUS_NOTIFICATION_IFACE, \
    DEFAULT_SPOTIFY_ICON


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