import os


class ScreenshotTaker(object):
    def __init__(self):
        """
        Thanks to https://github.com/emre/lama for the idea to use these commands
        :return:
        """
        self.__take_screenshot = 'scrot -sb %s'
        self.__put_on_clipboard = 'echo %s|xsel -bi'
        self.__notify_client = 'notify-send -a "Dropbox Screenshot" "%s"'

    def put_on_clipboard(self, url):
        os.system(self.__put_on_clipboard % url)

    def take_screenshot(self, name, path):
        os.chdir(path)
        os.system(self.__take_screenshot % name)

    def notify_client(self, link):
        os.system(self.__notify_client % link)
