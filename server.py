#!/usr/bin/env python3
import json
from concurrent import futures
import time
import grpc

import common.system_protos.basic_system_call_pb2_grpc as basic_system_call_grpc
from common.mainlogger import MainLoggerSingleton
from common.conf.ConfigControl import ConfigObj
from common.system_response import ResponseSingleton
from service.command_dispatcher import Dispatcher

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    basic_system_call_grpc.add_BasicSystemCallServicer_to_server(ServiceMain(), server)
    server.add_insecure_port('[::]:22223')
    print("gRPC 서버가 22223 포트에서 실행 중입니다.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
