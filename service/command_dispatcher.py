#!/usr/bin/env python3

from common.mainlogger import MainLoggerSingleton
from control.customer_control import CustomerControl


class Dispatcher:
    def __init__(self):
        self._log = MainLoggerSingleton().logger()
        self._customer_manager = CustomerControl()

    # 고객 등록
    def do_register_customer(self, argument):
        return self._customer_manager.register(argument)

    # 고객 조회
    def do_get_customer(self, argument):
        return self._customer_manager.find_user_by_obj_id(argument['_id'])

    # 고객 정보 수정
    def do_update_customer(self, argument):
        return self._customer_manager.update(argument['_id'], argument)

    # 고객 삭제
    def do_delete_customer(self, argument):
        return self._customer_manager.delete(argument['_id'])

    # 고객 로그인
    def do_login_customer(self, argument):
        return self._customer_manager.login(argument)

    # 고객 로그아웃
    def do_logout_customer(self, argument):
        return self._customer_manager.logout(argument)

    # 명령어 분배 메서드
    def dispatch(self, cmd: str, argument):
        if cmd is not None:
            method_name = 'do_' + cmd.lower()
            if hasattr(self, method_name):
                method = getattr(self, method_name)
                ret, code = method(argument)
            else:
                ret = {
                    'system_error': f'invalid message[{cmd}]',
                    'argument': argument
                }
                code = 500
        else:
            ret = {'system_error': 'command message is None'}
            code = 500
        return ret, code
