#!/usr/bin/python3

import signal
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator
gi.require_version('Notify', '0.7')
from gi.repository import Notify as notify

import subprocess

APPINDICATOR_ID = 'airpods_appindicator'
notification_icon = './airpods_icon.svg'
indicator_icon = './airpods_icon_alt.svg'

notification_icon_path = os.path.abspath(notification_icon)
indicator_icon_path = os.path.abspath(indicator_icon)

def build_menu():
    menu = gtk.Menu()
    item_connect = gtk.MenuItem(label='Connect Airpods')
    item_connect.connect('activate', connect)
    menu.append(item_connect)
    item_disconnect = gtk.MenuItem(label='Disconnect Airpods')
    item_disconnect.connect('activate', disconnect)
    menu.append(item_disconnect)
    item_separator = gtk.SeparatorMenuItem()
    menu.append(item_separator)
    item_quit = gtk.MenuItem(label='Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(_):
    notify.uninit()
    gtk.main_quit()

def try_connect():
    output = subprocess.run(["bash", "./airpods_connect.sh"], capture_output=True)
    if 'Connection successful' in output.stdout.decode():
        return 'Connection successful!'
    else:
        return 'Connection failed!'

def try_disconnect():
    output = subprocess.run(["bash", "./airpods_disconnect.sh"], capture_output=True)
    if 'Successful disconnected' in output.stdout.decode():
        return 'Successful disconnected!'
    else:
        return 'Disconnection failed!'

def connect(_):
    notify.Notification.new("Airpods", try_connect(), notification_icon_path).show()

def disconnect(_):
    notify.Notification.new("Airpods", try_disconnect(), notification_icon_path).show()

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, indicator_icon_path, appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
