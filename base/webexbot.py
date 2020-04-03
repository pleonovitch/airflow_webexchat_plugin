# Copyright 2019 Kohl's Department Stores, Inc.
"""Simple implementation of send message / send file functionality for cisco webex teams."""
import sys
import requests
import json
import os

SEND_FILE_SUPPORT = True
try:
    import magic
    from requests_toolbelt import MultipartEncoder
except ImportError:
    SEND_FILE_SUPPORT = False


class WebexBot():
    """Basic class that implements required functionality."""
    def __init__(self, access_token, proxies=None):
        self._access_token = access_token
        self._current_space = None
        self._room = None
        self._room_id = None
        self._rooms = dict()
        self._proxies = proxies

        # list rooms to see if access_token is working
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self._access_token)}
        try:
            r = requests.get('https://api.ciscospark.com/v1/rooms/', headers=headers, proxies=self._proxies)
            if r.status_code != 200:
                self._access_token = None
                raise WebexBotException

        except Exception as e:
            self._access_token = None
            raise WebexBotException

    def assign_room(self, room_name):
        """designates bot to chat space specified by room_name."""
        if self._access_token is None:
            raise WebexBotException

        if room_name in self._rooms:
            self._room_id = self._rooms[room_name]
            return

        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self._access_token)}
        try:
            r = requests.get('https://api.ciscospark.com/v1/rooms/', headers=headers, proxies=self._proxies)
            if r.status_code != 200:
                raise WebexBotException
        except Exception as e:
            raise WebexBotException
        try:
            d_raw  = r.text
            d = json.loads(d_raw)
            for item in d['items']:
                if item['title'] == room_name:
                    self._room = room_name
                    self._room_id = item['id']
                    self._rooms[room_name] = item['id']
                    return
            raise WebexBotException('Unable to locate {} space as one those available to bot'.format(room_name))
        except Exception as e:
            raise WebexBotException

    def send_message_to_room(self, message, md_message=None):
        """Sends message to currently assigned chat space."""
        if self._access_token is None or self._room_id is None:
            raise WebexBotException

        payload = {'roomId': self._room_id, 'text': message, 'markdown': md_message}
        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(self._access_token)}
        try:
            r = requests.post('https://api.ciscospark.com/v1/messages/', headers=headers, json=payload, proxies=self._proxies)
            if r.status_code != 200:
                raise WebexBotException
        except Exception as e:
            raise WebexBotException()

    def send_file_to_room(self, annotation, file_path, file_name=None ):
        """Sends file located in file_path to currently assigned chat space to be received as file_name."""
        if not SEND_FILE_SUPPORT:
            raise WebexBotException('send_file_to_room is not supported in this run time environment')

        if self._access_token is None or self._room_id is None:
            raise WebexBotException('access token or room_id is not available')

        #todo: if file name is not specified extract it from the path
        if file_name is None:
            file_name = os.path.basename(file_path)

        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file( file_path )

            m_fields = {'roomId': self._room_id,
                        'text': annotation,
                        'files': (file_name, open(file_path, 'rb'), file_type)}

            m = MultipartEncoder(fields = m_fields)
            headers = {'content-type': m.content_type, 'Authorization': 'Bearer {}'.format(self._access_token)}
            r = requests.post(url='https://api.ciscospark.com/v1/messages/', data=m, headers=headers, proxies=self._proxies)
            if r.status_code != 200:
                raise WebexBotException

        except Exception as e:
            raise WebexBotException

class WebexBotException(Exception):
    pass

if __name__ == "__main__":
    print("Not supposed to be executed directly!")
    sys.exit(1)