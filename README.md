# Airflow plugin for Webex chat and file transmission transactions

Provides means to send textual and file content into Cisco Webex Team space.

## Installation

General installation of plugin should be done in accordance with Airflow documentation: [Airflow plugins](https://airflow.apache.org/plugins.html)

__Required modules in Airflow Virtual environment:__
* requests
* requests_toolbelt
* magic


__Installation process:__
* Make sure that required python modules are installed in Airflow virtual environment
* Create **webex_chat_plug** folder in **$AIRFLOW_HOME/plugins**
* Copy all files from this repository in this new folder
## Documentation

### Hooks
#### WebexchatHook
Handles processing of connector information and basic transport

### Operators
#### WebexchatSendMessageOperator
Sends communication to chat space
Parameters

Name | Description | Required
--- | ----------- | ---------
webexchat_conn_id | Connection ID | Yes
space | Chat space where messaage must be sent (Bot must be invited into that space ) | Yes
message | Text of message | Yes
md_message | Message in markdown format | No
fail_on_error | Indicator of Operator should fail in case on failure. It is set to False by default to prevent chat operator to fail dag | No

if both **message** and **md_message** are present, **md_message** will be used for content of communication

#### WebexchatSendFileOperator
Sends communication to chat space
Parameters

Name | Description | Required
--- | ----------- | ---------
webexchat_conn_id | Connection ID | Yes
space | Chat space where messaage must be sent (Bot must be invited into that space ) | Yes
file_path | Full file path | Yes
annotation | Optional message that will appear along with file delivery message | No
fail_on_error | Indicator of Operator should fail in case on failure. It is set to False by default to prevent chat operator to fail dag | No


### Notes on connector
Using Airflow UI (Admin/Connections), you must create connector (refered to by **webexchat_conn_id** in operator call) of type HTTP with the following elements filled up

| Name | Description | Required |
| --- | ----------- | ---------|
| Password | Webexchat Bot token | Yes |
| Extra | Additional information | No |

**Extra** is JSON formatted information that allows you to specify outbound HTTP proxy configuaration
For example:
```bash
{
"proxies": {"http":"http://proxy.server.com:3128", "https":"https://proxy.server.com:3128"}
}
```


### Usage example of 'send message' operator, errors will be ignored
```
from airflow.operators.webex_chat_plugin import WebexchatSendMessageOperator
...

send_message_to_webex = WebexchatSendMessageOperator(task_id='send_message_to_webex',
                                         webexchat_conn_id = 'webex_chat',
					                     space='test_space',
                                         message ='test message from airflow',
                                         md_message = 'test **message** from airflow is **important**',
                                         dag=dag
                                         )
```


### Usage example of 'send file' operator, error will fail operator
```
from airflow.operators.webex_chat_plugin import WebexchatSendFileOperator
...

send_file_to_webex = WebexchatSendFileOperator(task_id='send_file_to_webex',
                                         webexchat_conn_id = 'webex_chat',
                                         space='test_space',
                                         annotation ='Here is your file',
                                         file_path = '/tmp/path/to/your/file.txt',
                                         fail_on_error = True,
                                          dag=dag
                                         )
```
