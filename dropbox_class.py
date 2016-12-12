import dropbox
import os


class Dropbox(object):
    def __init__(self):
        try:
            self.__app_keys = open(
                os.path.expanduser('~') +
                '/Dropbox/.dropbox_screenshot_keys', 'r'
            )
        except IOError:
            print('You need to get the dropbox app keys from me'
                  ' (Josh Manning), or create your own \'Dropbox App\'')
            return

        try:
            self.__access_token = open(
                os.path.expanduser('~') +
                '/Dropbox/.secret_auth', 'r'
            ).readline()
        except IOError:
            self.__create_auth()

        self.client = dropbox.client.DropboxClient(self.__access_token)

    def __create_auth(self):
        flow = dropbox.client.DropboxOAuth2FlowNoRedirect(
            self.__app_keys.readline()[:-1],
            self.__app_keys.readline()[:-1]
        )
        self.__app_keys.close()

        authorize_url = flow.start()
        print('1. Go to: ' + authorize_url)
        print('2. Click "Allow" (you might have to log in first)')
        print('3. Copy the authorization code.')
        code = raw_input("Enter the authorization code here: ").strip()
        self.__access_token, user_id = flow.finish(code)
        try:
            auth_file = open(os.path.expanduser('~') + '/Dropbox/.secret_auth', 'w')
        except IOError:
            print("Change the file names to not use dropbox.")
            return
        auth_file.write(self.__access_token)
        auth_file.close()

    def put_file(self, path, name):
        file_upload = open(path + '/' + name, 'rb')
        self.client.put_file('/Screenshots/' + name, file_upload)
        file_upload.close()

    def get_link_for_file(self, path):
        return self.client.share(path, False)['url']
