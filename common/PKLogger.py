# -*- coding: utf-8 -*-

import logging
from logging import handlers
# import json
from common.json_control import json_dump
import os
# from datetime import datetime
# from dateutil.tz import tzlocal
from fluent import handler
from fluent import asynchandler as handler_async
import msgpack
from io import BytesIO
import sys

'''custom_format = {
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'type': '%(levelname)s',
    'stack_trace': '%(exc_text)s'
}'''


def IsKey(config, key, default_value):
    if config is None:
        res = default_value
    else:
        if key in config.keys():
            res = config[key]
        else:
            res = default_value
    return res


class PKLogger():
    def __init__(self, name, config=None):
        _log_path = IsKey(config, 'path', './')
        if not os.path.exists(_log_path): os.makedirs(_log_path)
        _StreamHandlerUse = IsKey(config, 'stream_handler_use', True)
        _log_level = IsKey(config, 'log_level', logging.DEBUG)
        _SyslogHandlerUse = IsKey(config, 'syslog', False)
        _SyslogHost = IsKey(config, 'syslog_host', '127.0.0.1')
        _SyslogPort = IsKey(config, 'syslog_port', 514)
        _UdplogHandlerUse = IsKey(config, 'udplog', False)
        _UdplogHost = IsKey(config, 'udplog_host', '127.0.0.1')
        _UdplogPort = IsKey(config, 'udplog_port', 9021)
        _FluentdHandlerUse = IsKey(config, 'fluentd', False)
        _FluentHost = IsKey(config, 'fluentd_host', '127.0.0.1')
        _FluentPort = IsKey(config, 'fluentd_port', 24224)

        self._name = name
        # self.local_tz = tzlocal()
        logging.basicConfig()
        self.logger = logging.getLogger(self._name)
        self.logger.setLevel(_log_level)

        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s(%(filename)s:%(lineno)d) - %(message)s')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')
        self.logger.propagate = 0  # 상위 logger로 전파되는 것 막기

        if not self.logger.handlers:
            ''' stream handler '''
            if _StreamHandlerUse:
                _StreamHandler = logging.StreamHandler()
                _StreamHandler.setFormatter(formatter)
                self.logger.addHandler(_StreamHandler)

            _filename = "%s/%s.log" % (_log_path, name)

            ''' file handler '''
            _log_max_size = 10 * 1024 * 1024
            _log_file_count = 20
            _FileHandler = logging.handlers.RotatingFileHandler(filename=_filename, maxBytes=_log_max_size,
                                                                backupCount=_log_file_count)

            # file_handler = logging._FileHandler(filename)
            _FileHandler.setFormatter(formatter)
            self.logger.addHandler(_FileHandler)

            ''' UDP handler'''
            if _UdplogHandlerUse:
                _UdpHandler = logging.handlers.DatagramHandler(_UdplogHost, _UdplogPort)
                _UdpHandler.setFormatter(formatter)
                self.logger.addHandler(_UdpHandler)

            ''' Syslog handler'''
            if _SyslogHandlerUse:
                _SyslogHandler = logging.handlers.SysLogHandler(_SyslogHost, _SyslogPort)
                _SyslogHandler.setFormatter(formatter)
                self.logger.addHandler(_SyslogHandler)

            ''' fluent handler'''
            if _FluentdHandlerUse:
                custom_format = {
                    'time': '%(asctime)s',
                    'level': '%(levelname)s',
                    # 'host': '%(hostname)s',
                    # 'where': '%(module)s.%(funcName)s',
                    'module': '%(name)s',
                    'message': '%(message)s',
                    # 'stack_trace': '%(exc_text)s'
                }
                _FluentdHandler = handler_async.FluentHandler('service', host=_FluentHost, port=_FluentPort,
                                                              buffer_overflow_handler=self.overflow_handler,
                                                              nanosecond_precision=True)
                formatter = handler.FluentRecordFormatter(custom_format, datefmt="%Y-%m-%d %H:%M:%S %z")
                _FluentdHandler.setFormatter(formatter)
                self.logger.addHandler(_FluentdHandler)

    def overflow_handler(self, pendings):
        unpacker = msgpack.Unpacker(BytesIO(pendings))
        for unpacked in unpacker:
            print(unpacked)
            # print >> sys.stderr, unpacked

    def setLevel(self, Level):
        self.logger.setLevel(Level)

    def _structured(self, method, level, event, path=None, user_id=None, user_ip=None, message=None, raw_json=None):
        log_body = {
            'user_id': user_id,
            'user_ip': user_ip,
            'method': method,
            'path': path,
            'level': logging.getLevelName(level),
            'event': event,
            'message': message,
            'raw_json': raw_json,
        }
        self.logger.log(level, json_dump(log_body))

    def info_json(self, method, event, path=None, user_id=None, user_ip=None, message=None, raw_json=None):
        self._structured(user_id=user_id, path=path, user_ip=user_ip, method=method, level=logging.INFO, event=event, message=message, raw_json=raw_json)

    def warning_json(self, method, event, path=None, user_id=None, user_ip=None, message=None, raw_json=None):
        self._structured(user_id=user_id, path=path, user_ip=user_ip, method=method, level=logging.WARN, event=event, message=message, raw_json=raw_json)

    def error_json(self, method, event, path=None, user_id=None, user_ip=None, message=None, raw_json=None):
        self._structured(user_id=user_id, path=path, user_ip=user_ip, method=method, level=logging.ERROR, event=event, message=message, raw_json=raw_json)

    def debug_json(self, method, event, path=None, user_id=None, user_ip=None, message=None, raw_json=None):
        self._structured(user_id=user_id, path=path, user_ip=user_ip, method=method, level=logging.DEBUG, event=event, message=message, raw_json=raw_json)

    def critical_json(self, method, event, path=None, user_id=None, user_ip=None, message=None, raw_json=None):
        self._structured(user_id=user_id, path=path, user_ip=user_ip, method=method, level=logging.CRITICAL, event=event, message=message, raw_json=raw_json)

    def info(self, log_data):
        self.logger.log(logging.INFO, log_data)

    def warning(self, log_data):
        self.logger.log(logging.WARN, log_data)

    def error(self, log_data):
        self.logger.log(logging.ERROR, log_data)

    def debug(self, log_data):
        self.logger.log(logging.DEBUG, log_data)

    def critical(self, log_data):
        self.logger.log(logging.CRITICAL, log_data)


if __name__ == '__main__':
    config = {}
    config['path'] = './'
    config['stream_handler_use'] = True
    log = PKLogger('test', config)
    log.setLevel("DEBUG")

    log.debug('debug')
    log.info('info')
    log.warning('warning')
    log.error('error')
    log.critical('critical')