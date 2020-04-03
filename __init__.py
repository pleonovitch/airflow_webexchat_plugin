# Copyright 2019 by Pavel Leonovitch
from airflow.plugins_manager import AirflowPlugin
from webex_chat_plugin.hooks.webex_chat_hook import WebexchatHook
from webex_chat_plugin.operators.webex_chat_operator import WebexchatSendMessageOperator, \
                                                            WebexchatSendFileOperator


class WebexchatPlugin(AirflowPlugin):
    name = "webex_chat_plugin"
    operators = [WebexchatSendMessageOperator, WebexchatSendFileOperator ]
    hooks = [WebexchatHook]
