###!/usr/bin/env python3
import json
from concurrent import futures
import time
import grpc

import common.system_protos.basic_system_call_pb2_grpc as basic_system_call_grpc
from common.mainlogger import MainLoggerSingleton
from common.conf.ConfigControl import ConfigObj
from common.system_response import ResponseSingleton
from service.command_dispatcher import Dispatcher


class ServiceMain(basic_system_call_grpc.BasicSystemCall):
    def __init__(self):
        self._log = MainLoggerSingleton().logger()
        self.command_dispatcher = Dispatcher()

    def _ext_command(self, req_body):
        if 'header' in req_body:
            if 'message' in req_body['header']:
                return req_body['header']['message']
        return None

    def _ext_body(self, req_body):
        if 'body' in req_body:
            return req_body['body']
        return None

    def SystemRequest(self, request, context):
        self._log.info_json(method='SystemRequest', event='start')
        start = time.time()
        response = self._executor(request.message)
        tact = round(time.time() - start, 6)
        self._log.info_json(method='SystemRequest', event='end',
                            raw_json={
                                'elapsed_time': tact,
                                'status_code': response.statusCode,
                                'statusMessage': response.statusMessage,
                                'returnBody': response.returnBody,
                            })

        return response

    def _executor(self, request_message):
        try:
            req = json.loads(request_message)

            cmd = self._ext_command(req)
            ResponseSingleton().set_request(req)
            body = self._ext_body(req)
            self._log.info_json(method='_executor', event='run',
                                raw_json={
                                    'command': cmd,
                                    'argument': body
                                })

            ret, code = self.command_dispatcher.dispatch(cmd, body)
            return ResponseSingleton().make_res_body(ret, code)
        except Exception as e:
            return ResponseSingleton().make_res_body({'exception': str(e)}, 500)


def serve():
    config = ConfigObj()
    logger = MainLoggerSingleton().logger()
    port = config.getValue("app", "port")
    # header_validator = RequestHeaderValidatorInterceptor(
    #     'one-time-password', '42', grpc.StatusCode.UNAUTHENTICATED,
    #     'Access denied!')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # , interceptors = (header_validator,))
    basic_system_call_grpc.add_BasicSystemCallServicer_to_server(
        ServiceMain(), server)
    address = '[::]:{}'.format(port)
    server.add_insecure_port(address)
    logger.info('start server - {}'.format(address))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    conf_file = './config.toml'

    config = ConfigObj()
    config.loadingConfigFile(conf_file)
    serve()
