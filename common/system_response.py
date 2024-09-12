from datetime import datetime, date

from bson import ObjectId

import common.system_protos.basic_system_call_pb2 as basic_system_call
from common.SingletonTemplate import Singleton
from common.json_control import json_dump
from common.mainlogger import MainLoggerSingleton


def json_encoder(o):
    if isinstance(o, (date, datetime)):
        return o.strftime("%Y-%m-%d %H:%M:%S.%f")
    elif isinstance(o, ObjectId):
        return str(o)


class SystemResponse:
    def __init__(self):
        self._request = None
        self._log = MainLoggerSingleton().logger()

    def set_request(self, header):
        self._request = header

    def make_res_body(self, return_body, code):
        now = datetime.now()

        code_category = int(code / 100)
        if code_category == 2:
            status_message = 'success'
        elif code_category == 5:
            status_message = 'system error'
        else:
            status_message = 'fail'

        response = {
            'header': {
                "message": self._request['header']['message'],
                "datetime": now.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "from_module": "service-spc-result-manager",
                "message_type": "response",
                "transaction_id": self._request['header']['transaction_id']
            },
            'body': self._request['body'],
            "response": {
                "status_code": code,
                "status_message": status_message,
                "return_body": return_body
            }
        }

        if return_body is None:
            response['body']['return_body'] = {}

        res = basic_system_call.SystemResponse()
        res.statusCode = code
        res.statusMessage = status_message
        res.returnBody = json_dump(response)
        return res


class ResponseSingleton(SystemResponse, metaclass=Singleton):
    pass
