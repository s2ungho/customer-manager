from __future__ import print_function

import json
import time
import grpc

import common.system_protos.basic_system_call_pb2 as system_grpc
import common.system_protos.basic_system_call_pb2_grpc as system_call
from common.json_control import json_dump

HOST_BASE = '127.0.0.1:22223'
grpc_options = [
    ('grpc.max_send_message_length', 86378919),
    ('grpc.max_receive_message_length', 86378919),
]

sample_req = {
    "header": {
        "message": "get_customer",  # 고객 조회 명령어
        "datetime": time.strftime('%Y-%m-%d %H:%M:%S'),
        "from_module": "client01",
        "message_type": "request",
        "transaction_id": f"{time.strftime('%Y%m%d%H%M%S')}_client01"
    },
    "body": {
        "_id": "고객의 ObjectId 값"  # 조회할 고객 ID
    }
}


def send_request(request_body, host=HOST_BASE):
    with grpc.insecure_channel(host, options=grpc_options) as channel:
        stub = system_call.BasicSystemCallStub(channel)
        start = time.time()
        req_msg = system_grpc.RequestMessage()
        req_msg.message = json_dump(request_body)
        feature = stub.SystemRequest(req_msg)
        res = json.loads(feature.returnBody)
        return res


if __name__ == '__main__':
    res = send_request(sample_req, host=HOST_BASE)
    return_body = res['response']['return_body']
    status_code = res['response']['status_code']
    print(return_body)
    print(f'code : {status_code}')

    print('end')
