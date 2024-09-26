import http
import os
import connexion
from http import HTTPStatus
from connexion import request
from common.decorator import timed
from common.conf.ConfigControl import ConfigObj
from common.mainlogger import MainLoggerSingleton
from control.customer_control import CustomerControlSingleton
from flask_cors import CORS
from models.user import User
import requests
import re
import bcrypt

from interface.grpc_interface import GrpcInterface

"""
=======================================================================
api customer manager
=======================================================================
"""


@timed
def get_list():
    if not request.is_json:
        return "A JSON body is required", 500
    req = request.get_json()
    print(req)
    # result, code = customerCtrl.get_list(req)

    grpc_result = interface.send_request('127.0.0.1', 22222, 'get_list', req)
    result, code = interface.service_response(grpc_result)

    return result, code

@timed
def get_customer(id):
    req = request.get_json()
    #result, code = customerCtrl.find_user_by_obj_id(id)
    result, code = interface.send_request('127.0.0.1', 22222, 'get_customer', req)
    if code != 200:
        return {"message": "Customer not found"}, 404
    return result, code

@timed
def register():
    if not request.is_json:
        return "A JSON body is required", 500
    req = request.get_json()
    #result, code = customerCtrl.register(req)
    #result, code = interface.send_request('127.0.0.1', 22222, 'get_list', req)
    grpc_result = interface.send_request('127.0.0.1', 22222, 'register_customer', req)
    result, code = interface.service_response(grpc_result)
    return result, code

@timed
def delete():
    if not request.is_json:
        return "A JSON body is required", 500

    req = request.get_json()
    customer_id = req.get('_id')

    if not customer_id:
        return {"message": "Customer ID is required"}, 400

    #result, code = customerCtrl.delete(customer_id)
    #result, code = interface.send_request('127.0.0.1', 22222, 'delete_customer', req)
    grpc_result = interface.send_request('127.0.0.1', 22222, 'delete_customer', req)
    result, code = interface.service_response(grpc_result)

    return result, code

@timed
def update():
    if not request.is_json:
        return "A JSON body is required", 500

    req = request.get_json()
    customer_id = req.get('_id')  # 고객 ID를 요청에서 가져옴

    if not customer_id:
        return {"message": "Customer ID is required"}, 400

    # 고객 정보를 업데이트하는 함수 호출
    #result, code = customerCtrl.update(customer_id, req)
    #result, code = interface.send_request('127.0.0.1', 22222, 'update_customer', req)
    grpc_result = interface.send_request('127.0.0.1', 22222, 'update_customer', req)
    result, code = interface.service_response(grpc_result)

    return result, code

# 로그인
def login():
    req = connexion.request.get_json()
    email = req.get("email")
    password = req.get("password")
    print(email)
    print(password)
    #user, code = customerCtrl.find_user_by_email(email)
    #user, code = interface.send_request('127.0.0.1', 22222, 'login_customer', req)
    grpc_result = interface.send_request('127.0.0.1', 22222, 'login_customer', req)
    user, code = interface.service_response(grpc_result)
    print(user)
    print(code)
    print("Stored hash:", user['password_hash'])

    password = "bbbb"  # 사용자가 입력한 비밀번호
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print("Input password hash:", hashed.decode('utf-8'))

    if code == 200:
        # 입력한 비밀번호와 DB에 저장된 해시된 비밀번호 비교
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):  # 비밀번호 비교
            return {"message": "Login successful"}, 200
        else:
            return {"message": "Invalid credentials"}, 400

    return {"message": "Invalid credentials"}, 400

# 로그아웃
def logout():
    return {"message": "Logout successful"}, 200

# =======================================================================
if "MODE" in os.environ:
    env_mode = os.environ["MODE"]
elif "mode" in os.environ:
    env_mode = os.environ["mode"]
else:
    env_mode = 'dev'

if env_mode == 'dev':
    conf_file = 'config_dev.toml'
else:
    conf_file = './config.toml'

config = ConfigObj()
config.loadingConfigFile(conf_file)
# customerCtrl = CustomerControlSingleton()
mainLog = MainLoggerSingleton()
_log = mainLog.logger()

interface = GrpcInterface()

app = connexion.App(__name__, host=config.getValue('app', 'host'), port=config.getValue('app', 'port'),
                    specification_dir='swagger/')
CORS(app.app)
print('# connexion.App')

app.add_api('swagger.yaml', resolver=connexion.resolver.RestyResolver('app'))
print('# app.add_api')

if __name__ == '__main__':
    print('# __main__ : start')
    app.run(host='0.0.0.0', port=5001)#debug=False, use_reloader=False)
    # app.run(debug=True, use_reloader=True)
