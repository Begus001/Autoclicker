from pynput import keyboard, mouse
from gi.repository import Gtk
import os
import time
import gi
import threading
gi.require_version("Gtk", "3.0")

cps = 1

combi = list()

clicked = list()
keys_pressed = list()

enabled = False
stop = False
combi_mode = False

builder = Gtk.Builder()
builder.add_from_file("form.glade")

win_main = builder.get_object("win_main")
header_bar = builder.get_object("header_bar")


def klik(x, y, button, pressed):
    global clicked, enabled, combi_mode, combi, keys_pressed

    if pressed is True:
        clicked.append(button)
    elif button in clicked:
        clicked.remove(button)

    if combi_mode is True:

        if button not in combi:
            print("appending {}".format(button))
            combi.append(button)

        print("clicked {}".format(clicked))

        if len(clicked) is 0:
            combi_mode = False
            print("combi {}".format(combi))
            sub = ""
            for current in combi:
                sub += str(current) + " + "
            header_bar.set_subtitle(sub[:len(sub)-3])
            return

    if len(combi) <= 0:
        return

    for current in combi:
        if current not in clicked:
            return

    enabled = not enabled
    control = mouse.Controller()
    control.press(mouse.Button.middle)
    control.release(mouse.Button.middle)


def key_press(key):
    global keys_pressed, combi, combi_mode, enabled
    keys_pressed.append(key)
    if keyboard.Key.esc in keys_pressed:
        enabled = False
        combi = list()
        combi_mode = False
        print("combi mode aborted")
        return


def key_release(key):
    global keys_pressed
    if key in keys_pressed :
        keys_pressed.remove(key)


def main_loop(name):
    while True:
        if stop is True:
            return

        if enabled is True and combi_mode is False:
            os.popen("xdotool click 1")
            print("klik")
            time.sleep(1 / cps)


def destroy(arg):
    global stop
    stop = True
    Gtk.main_quit()
    exit()


def bt_set_combi_clicked_cb(btn):
    global combi_mode, combi, enabled
    combi = list()
    enabled = False
    print("combi mode")
    combi_mode = True


def spbt_cps_value_changed_cb(spbt):
    global cps
    cps = spbt.get_value_as_int()


win_main.show_all()
win_main.connect("destroy", destroy)

handlers = {
    "bt_set_combi_clicked_cb": bt_set_combi_clicked_cb,
    "spbt_cps_value_changed_cb": spbt_cps_value_changed_cb
}

builder.connect_signals(handlers)

mouse_listener = mouse.Listener(on_click=klik)
mouse_listener.start()

keyboard_listener = keyboard.Listener(on_press=key_press, on_release=key_release)
keyboard_listener.start()

x = threading.Thread(target=main_loop, args=(1,))
x.start()

Gtk.main()
