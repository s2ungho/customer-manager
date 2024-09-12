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
    result, code = customerCtrl.get_list(req)
    return result, code

@timed
def register():
    if not request.is_json:
        return "A JSON body is required", 500
    req = request.get_json()
    result, code = customerCtrl.register(req)
    return result, code

@timed
def delete():
    if not request.is_json:
        return "A JSON body is required", 500

    req = request.get_json()
    customer_id = req.get('_id')

    if not customer_id:
        return {"message": "Customer ID is required"}, 400

    result, code = customerCtrl.delete(customer_id)
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
    result, code = customerCtrl.update(customer_id, req)
    return result, code



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
customerCtrl = CustomerControlSingleton()
mainLog = MainLoggerSingleton()
_log = mainLog.logger()

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
