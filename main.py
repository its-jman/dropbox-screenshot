import dropbox_class
import screenshot_class
import datetime
import os
from Xlib import display
from Xlib import X
from Xlib.ext import record
from Xlib.protocol import rq


currently_pressed = []
buttons = [37, 95]

dropbox_path = os.path.expanduser('~') + '/Dropbox/Screenshots/'
tmp_path = os.path.expanduser('~') + '/.tmp'

screenshot = screenshot_class.ScreenshotTaker()
dropbox = dropbox_class.Dropbox()


def take_screenshot(name):
    screenshot.take_screenshot(name, tmp_path)

    try:
        dropbox.put_file(tmp_path, name)
    except IOError:
        print('Screenshot cancelled.')
        return

    os.remove(tmp_path + '/' + name)

    dropbox_link = dropbox.get_link_for_file('/Screenshots/' + name)

    screenshot.put_on_clipboard(dropbox_link)
    screenshot.notify_client(dropbox_link)


def get_name():
    return datetime.datetime.now().strftime("%Y_%M_%d_%H%M%s.png")


"""
-----------------------REQUIREMENTS FOR KEY HANDLING-----------------------------------------------
Adapted from original post: http://pastebin.com/DwSyYTYn
"""


disp = display.Display()
root = disp.screen().root


def handler(reply):
    """ This function is called when a xlib event is fired """
    global currently_pressed

    data = reply.data
    while len(data):
        event, data = rq.EventField(None).parse_binary_value(data, disp.display, None, None)
        key_number = event.detail

        if event.type == X.KeyPress:
            if key_number in buttons:
                currently_pressed += [key_number]
                if len(currently_pressed) == 2:
                    is_full = filter(lambda x: x in buttons, currently_pressed)
                    if False not in is_full:
                        take_screenshot(get_name())
        elif event.type == X.KeyRelease:
            if key_number in currently_pressed:
                currently_pressed.remove(key_number)


ctx = disp.record_create_context(
    0,
    [record.AllClients],
    [{
        'core_requests': (0, 0),
        'core_replies': (0, 0),
        'ext_requests': (0, 0, 0, 0),
        'ext_replies': (0, 0, 0, 0),
        'delivered_events': (0, 0),
        'device_events': (X.KeyReleaseMask, X.ButtonReleaseMask),
        'errors': (0, 0),
        'client_started': False,
        'client_died': False,
    }]
)


disp.record_enable_context(ctx, handler)
disp.record_free_context(ctx)


while True:
    current_event = root.display.next_event()


"""
-------------------END REQUIREMENTS FOR KEY HANDLING-----------------------------------------------
"""
