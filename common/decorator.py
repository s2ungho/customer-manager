# def AddRequestResultTags(LoggerDelegate):
#     def SetDecorator(func):
#         def Wrapper(*args, **kwargs):
#             Response = func(*args, **kwargs)
#             if Response.Status_code == 200:
#                 LoggerDelegate.info("{} - success".format(func.__name__))
#             else:
#                 LoggerDelegate.error("{} - fail".format(func.__name__))
#         return Wrapper
#     return SetDecorator

from flask import request
import time
from functools import wraps

from common.mainlogger import MainLoggerSingleton


def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        _main_logger = MainLoggerSingleton().logger()
        try:
            req_body = None
            if 'req_body' in kwargs:
                req_body = kwargs['req_body']

            user_id = None
            user_ip = None
            if req_body is not None and 'user_id' in req_body:
                user_id = req_body['user_id']
            if req_body is not None and 'user_ip' in req_body:
                user_ip = req_body['user_ip']

            start = time.time()
            message = "{} .................. start".format(func.__name__)
            _main_logger.info_json(user_id=user_id, user_ip=user_ip,
                                   method=func.__name__,
                                   event='start',
                                   message=message)
            result, code = func(*args, **kwargs)
            end = time.time()
            message = "{} .................. end [{}s]".format(func.__name__, round(end - start, 6))
            _main_logger.info_json(user_id=user_id, user_ip=user_ip,
                                   method=func.__name__,
                                   event='end',
                                   message=message,
                                   raw_json={"result": result, "code": code})
            return result, code
        except Exception as e:
            _main_logger.critical_json(
                method=func.__name__,
                event='exception',
                message=str(e)
            )
            message = f'occurred message - {str(e)}'
            return {'message': message}, 500

    return wrapper


def self_logger_decorator(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            start = time.time()
            self._log.debug_json(
                method=func.__name__,
                event='start'
            )

            result, code = func(self, *args, **kwargs)
            tact = round(time.time() - start, 6)
            raw_json = {
                'elapsed_time': tact,
                'status_code': code
            }
            if code != 200:
                raw_json['status_message'] = result

            self._log.debug_json(
                method=func.__name__,
                event='end',
                raw_json=raw_json
            )
            return result, code
        except Exception as e:
            self._log.critical_json(
                method=func.__name__,
                event='exception',
                message=str(e)
            )
            raise

    return wrapper
