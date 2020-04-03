# Copyright 2019 Kohl's Department Stores, Inc.
# -*- coding: utf-8 -*-

from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from webex_chat_plugin.hooks.webex_chat_hook import WebexchatHook
from airflow.exceptions import AirflowException

class WebexchatSendMessageOperator(BaseOperator):
    """
       Webexchat send message
       :param webex_conn_id:            Connection for webex connectivity
       :type  webex_conn_id:            string
       :param space:                    Webex chat space
       :type  space:                    string
       :param message:                  text of message
       :type  message:                  string
       :param md_message:               text of message in markdown, optional. If present takes precendence of message
       :type  md_message:               string
       :param fail_on_error:            flag indicating if operator should fails in case of error. Optional, False by default
       :type  fail_on_error:            boolean
    """
    @apply_defaults
    def __init__(self,
                 webexchat_conn_id,
                 space,
                 message,
                 md_message=None,
                 fail_on_error = False,
                 *args, **kwargs):
        super(WebexchatSendMessageOperator, self).__init__(*args, **kwargs)

        if webexchat_conn_id is None:
            raise AirflowException('No valid Webex Chat Bot token nor webexchat_conn_id supplied.')

        self._webexchat_conn_id = webexchat_conn_id
        self._space = space
        self._message = message
        self._md_message = md_message
        self._fail_on_error = fail_on_error

    def execute(self, **kwargs):
            try:
                chat = WebexchatHook(self._webexchat_conn_id)
                chat.send_message(self._space, self._message, self._md_message)
            except Exception as e:
                if self._fail_on_error:
                    raise e
                else:
                    pass


class WebexchatSendFileOperator(BaseOperator):
    """
       Webexchat send file.
       :param webex_conn_id:            Connection for webex connectivity
       :type  webex_conn_id:            string
       :param space:                    Webex chat space
       :type  space:                    string
       :param file_path:                File path of file to be sent
       :type  file_path:                string
       :param annotation:               text of annotation that appears in file transmission
       :type  annotation:               string
       :param fail_on_error:            flag indicating if operator should fails in case of error. Optional, False by default
       :type  fail_on_error:            boolean
    """

    @apply_defaults
    def __init__(self,
                 webexchat_conn_id,
                 space,
                 file_path,
                 annotation='',
                 fail_on_error=False,
                 *args, **kwargs):
        super(WebexchatSendFileOperator, self).__init__(*args, **kwargs)

        if webexchat_conn_id is None:
            raise AirflowException('No valid Webex Chat Bot token nor webexchat_conn_id supplied.')

        self._webexchat_conn_id = webexchat_conn_id
        self._space = space
        self._file_path = file_path
        self._annotation = annotation
        self._fail_on_error = fail_on_error

    def execute(self, **kwargs):
        try:
            chat = WebexchatHook(self._webexchat_conn_id)
            chat.send_file(self._space, self._file_path, self._annotation)
        except Exception as e:
            if self._fail_on_error:
                raise e
            else:
                pass
