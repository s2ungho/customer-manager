from __future__ import print_function

import json
import pprint
from datetime import datetime

import grpc

import common.system_protos.basic_system_call_pb2 as system_grpc
import common.system_protos.basic_system_call_pb2_grpc as system_call
from common.PKLogger import PKLogger
from common.conf.ConfigControl import ConfigObj
from common.json_control import json_dump


class GrpcInterface:
    def __init__(self):
        config = ConfigObj()
        self._log = PKLogger('grpc-interface', config.getSectionDict('log'))
        # self._app_name = app_name
        # self._url = "{}:{}".format(host, port)
        self._max_message_length = 20971520
        self._grpc_options = [
            ('grpc.max_send_message_length', self._max_message_length),
            ('grpc.max_receive_message_length', self._max_message_length),
        ]

    def send_request(self, host, port, request_cmd, request_body):
        url = "{}:{}".format(host, port)
        packet = self._make_packet(request_cmd, request_body)
        with grpc.insecure_channel(url, options=self._grpc_options) as channel:
            self._log.debug_json(method='send_request',
                                 event='run',
                                 message='{} - {} 요청'.format(url, request_cmd),
                                 raw_json=request_body)
            stub = system_call.BasicSystemCallStub(channel)
            req_msg = system_grpc.RequestMessage()
            req_msg.message = json_dump(packet)
            feature = stub.SystemRequest(req_msg)
            res = json.loads(feature.returnBody)
            # print(json_dump(res))
            self._log.debug_json(method='send_request',
                                 event='run',
                                 message='{} - {}에 대한 응답'.format(url, request_cmd),
                                 raw_json=res)
            return res

    def _make_packet(self, request_cmd, req_body):
        now = datetime.now()
        trans_id = now.strftime('%Y%m%d%H%M%S%f_proxy')
        req_payload = {
            "header": {
                "message": request_cmd,
                "datetime": now.strftime('%Y-%m-%d %H:%M:%S.%f'),
                "from_module": "client01",
                "message_type": "request",
                "transaction_id": trans_id
            },
            "body": req_body
        }
        return req_payload

    def service_response(self, grpc_response):
        return grpc_response['response']['return_body'], grpc_response['response']['status_code']
