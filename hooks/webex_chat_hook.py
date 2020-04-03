# Copyright 2019 Kohl's Department Stores, Inc.
# -*- coding: utf-8 -*-
import requests
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowException
import json
from webex_chat_plugin.base.webexbot import WebexBot
from webex_chat_plugin.base.webexbot import WebexBotException


class WebexchatHook(BaseHook):

    def __init__(self, webexchat_conn_id ):
        conn = self.get_connection(webexchat_conn_id)
        if not getattr(conn, 'password', None):
            raise AirflowException('Missing token in webexchat  connection (password field)')
        self._token = conn.password

        if not getattr(conn, 'extra', None):
            self._proxies = None

        try:
            extra_j = json.loads( conn.extra)
            if not 'proxies' in extra_j:
                self._proxies = None
            else:
                self._proxies = extra_j['proxies']
        except ValueError:
            raise AirflowException('Invalid JSON content in webexchat connection (extra field)')


    def send_message(self, space, message, md_message=None):
            try:
                bot = WebexBot(access_token=self._token, proxies=self._proxies)
                bot.assign_room(space)
                bot.send_message_to_room(message=message, md_message=md_message)
            except WebexBotException as e:
                raise AirflowException('Failure to handle webex space: {}'.format(str(e)))


    def send_file(self, space, file_path, annotation):

            try:
                bot = WebexBot(access_token=self._token, proxies=self._proxies)
                bot.assign_room(space)
                bot.send_file_to_room( annotation=annotation,file_path=file_path )
            except WebexBotException as e:
                raise AirflowException('Failure to handle webex space: {}'.format(str(e)))
