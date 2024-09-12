import requests
import json
from common.PKLogger import PKLogger
from common.conf.ConfigControl import ConfigObj
from time import sleep

class RestWrap():
    def __init__(self):
        config = ConfigObj()
        self._Log = PKLogger('RestWrap', config.getSectionDict('log'))
        self.headers = {'content-type': 'application/json'}


    def _post(self, user_command_name, url, data: dict):
        return self.__command(requests.post, user_command_name, url, data)

    def _get(self, user_command_name, url):
        return self.__command(requests.get, user_command_name, url)

    def _patch(self, user_command_name, url, data: dict):
        return self.__command(requests.patch, user_command_name, url, data)

    def _delete(self, user_command_name, url):
        return self.__command(requests.delete, user_command_name, url)

    def __command(self, rest_method, user_command_name, url, data:dict = None):
        result = None
        code = 500
        for i in range(10):
            result, code = self.__rest_command(rest_method, user_command_name, url, data)
            if code != 500:
                break
            self._Log.critical("retry connection")
            sleep(2)

        if code == 500:
            print("################### critical fail", code)
        return result, code

    def __rest_command(self, rest_method, user_command_name, url, data:dict = None):
        try:
            if data is not None:
                json_data = json.dumps(data)
                response = rest_method(url, data=json_data, headers=self.headers, verify=False)
            else:
                # response = rest_method(url, headers=self.headers, verify=False)
                response = rest_method(url, verify=False)
            self.__Logging_Response(user_command_name, response)
            if response.status_code != 204:
                return response.json(), response.status_code
            else:
                return None, response.status_code

        except Exception as e:
            self._Log.critical('__command({}) Exception - {}'.format(user_command_name, str(e)))
            print(str(e))
            return str(e), 500



    def __Logging_Response(self, MethodName, Response):
        if Response is not None:
            if 200 <= Response.status_code < 300:
                self._Log.info("{} - Success".format(MethodName))
            else:
                self._Log.warning("{} - fail({})".format(MethodName, Response.status_code))
                self._Log.warning_json(MethodName,
                                       {'result code': str(Response.status_code), 'result': Response.json()})

        else:
            self._Log.critical("{} - Response is None".format(MethodName))