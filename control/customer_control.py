from datetime import datetime, timedelta

from bson import ObjectId

from common.SingletonTemplate import Singleton
from common.conf.ConfigControl import ConfigObj
from common.db.mongodb_control import MongodbControl
from common.decorator import self_logger_decorator
from common.dict_control import safe_dict_builder
from common.mainlogger import MainLoggerSingleton
from common.make_filter_time import make_filter_time
from models.user import User
import jwt
import re
import bcrypt


def _make_search_key(argument):
    try:
        payload = {}
        if 'filter' in argument:
            input_filter = argument['filter'].copy()
            safe_dict_builder(input_filter, payload, 'user_id')
            safe_dict_builder(input_filter, payload, 'active')
            safe_dict_builder(input_filter, payload, 'is_admin')

            if 'datetime_field' in input_filter:
                payload.update(make_filter_time(argument=input_filter))
            # print(payload)
            return payload
        else:
            return None
    except Exception as e:
        print(str(e))
        raise


class CustomerControl:
    def __init__(self):
        self.Users = []
        config = ConfigObj()
        collection_name = config.getValue('mongodb', 'collection')
        self._admin_user_id = config.getValue('app', 'admin_user_id')
        self._admin_password = config.getValue('app', 'admin_password')
        self._db_control = MongodbControl(collection_name)
        self._log = MainLoggerSingleton().logger()

    @self_logger_decorator
    def find_user_by_email(self, email):
        ref = {'email': email}
        return self._db_control.find_one(ref)

    @self_logger_decorator
    def find_user(self, user_id):
        ref = {'user_id': user_id}
        return self._db_control.find_one(ref)

    @self_logger_decorator
    def find_user_by_obj_id(self, obj_id):
        ref = {'_id': ObjectId(obj_id)}
        return self._db_control.find_one(ref)

    @self_logger_decorator
    def is_valid_id(self, user_id):
        if bool(re.match("^([a-zA-Z0-9_.]+)$", user_id)):
            return {'message': 'OK'}, 200
        else:
            return {'message': 'invalid id'}, 400

    @self_logger_decorator
    def is_logged_in(self, user: User):
        found_user, find_user_code = self.find_user(user.get_user_id())
        if find_user_code != 200:
            return {'message': 'User not found'}, find_user_code
        found_user = User(found_user)
        if not found_user.validate_password(user.get_password()):
            return {'message': 'Incorrect password. Please try again.'}, 401
        else:
            return {'is_logged_in': True}, 200

    @self_logger_decorator
    def is_admin(self, login_user: User):
        if login_user.get_user_id() == self._admin_user_id and login_user.get_password() == self._admin_password:
            return {
                       'user_id': self._admin_user_id,
                       'user_name': 'admin',
                       'password': '',
                       'is_admin': True
                   }, 200
        return {'result': 'The requested user does not have permission.'}, 403

    @self_logger_decorator
    def register(self, user_data):
        # 유효 검사
        required_fields = ["customer_name", "password_hash"]
        for field in required_fields:
            if field not in user_data:
                return {'message': f'{field} is required'}, 400

        # 비밀번호 해시 처리
        user_data['password_hash'] = bcrypt.hashpw(user_data['password_hash'].encode('utf-8'),
                                                           bcrypt.gensalt()).decode('utf-8')

        # MongoDB ObjectId 변환
        if "_id" in user_data:
            user_data["_id"] = ObjectId(user_data["_id"])

        # 날짜 필드 변환
        date_fields = ['created_datetime', 'updated_datetime', 'birth_date', 'signup_date', 'login_datetime',
                       'logout_datetime']
        for field in date_fields:
            if field in user_data:
                user_data[field] = datetime.strptime(user_data[field], '%Y-%m-%dT%H:%M:%SZ')

        # 생성날짜 수정 날짜 설정
        user_data['created_datetime'] = datetime.now()
        user_data['updated_datetime'] = datetime.now()

        #  데이터 삽입
        res, code = self._db_control.insert(user_data)
        if code == 200:
            return {'message': 'Customer registered successfully'}, 200
        else:
            return {'message': 'Registration failed'}, 500

    @self_logger_decorator
    def update(self, obj_id, user_info_to_update, admin_user=None):
        if '_id' in user_info_to_update:
            user_info_to_update.pop('_id')  # _id는 업데이트하지 않음

        # 객체 ID로 사용자를 찾음
        found_user, code = self.find_user_by_obj_id(obj_id)
        if code != 200:
            return {'message': 'User not found'}, code

        print("Found user data before update:", found_user)
        print("Update data:", user_info_to_update)

        # 사용자 객체 생성
        user = User(found_user)

        # 새 정보로 사용자 객체 업데이트
        user.update_property(user_info_to_update)
        update_body = user.to_dict()
        update_body['update_user'] = admin_user if admin_user else "admin"
        update_body['updated_datetime'] = datetime.now()

        print("Update body to be sent to MongoDB:", update_body)

        # MongoDB에서 업데이트 실행
        ref = {'_id': ObjectId(obj_id)}
        res, code = self._db_control.update(ref, update_body)

        res, code = self._db_control.update(ref, update_body)
        print("MongoDB 업데이트 결과:", res)

        if code == 200:
            return {'message': 'Customer updated successfully'}, 200
        else:
            return {'message': 'Update failed'}, 500

    @self_logger_decorator
    def delete(self, obj_id):
        try:
            ref = {'_id': ObjectId(obj_id)}
        except Exception as e:
            return {'message': 'Invalid Customer ID format'}, 400

        # 유효한지 확인
        found_user, code = self.find_user_by_obj_id(obj_id)
        if code != 200:
            return {'message': 'User not found'}, 404

        # 삭제
        res, code = self._db_control.delete(ref)
        print(res)
        print(code)
        if code == 200 or code == 204:
            return {'message': 'Customer deleted successfully'}, 200
        else:
            return {'message': 'Delete failed'}, 500

    @self_logger_decorator
    def login(self, user: User):
        found_user, code = self.find_user(user.get_user_id())

        if code != 200:
            return {'message': 'User not found'}, 404

        found_user = User(found_user)

        input_password_hash = bcrypt.hashpw(user.get_password().encode('utf-8'), bcrypt.gensalt())

        # 입력된 비밀번호와 해시된 비밀번호 비교
        if not bcrypt.checkpw(input_password_hash, found_user.get_password_hash().encode('utf-8')):
            return {'message': 'Incorrect password. Please try again.'}, 401

        ref = {'user_id': user.get_user_id()}
        update_body = {
            'login_datetime': datetime.now(),
            'active': True
        }

        res, code = self._db_control.update(ref, update_body)
        if code != 200:
            return res, code

        if 'password_hash' in res:
            del res['password_hash']
        return res, code

    @self_logger_decorator
    def logout(self, user: User):
        found_user, code = self.find_user(user.get_user_id())
        if code != 200:
            return {'message': 'User not found'}, 404

        ref = {'user_id': user.get_user_id()}
        update_body = {
            'logout_datetime': datetime.now(),
            'access_token': '',
            'active': False
        }
        return self._db_control.update(ref, update_body)

    @self_logger_decorator
    def get_list(self, argument, return_fields=None):
        ref = {}

        if 'filter' in argument:
            ref = _make_search_key(argument)
        total_count, code = self._db_control.count(ref)
        if code != 200:
            return {'total_count': total_count}, code

        page_size, page_num = None, None
        if 'page_size' in argument and 'page_num' in argument:
            page_size = argument["page_size"]
            page_num = argument["page_num"]
            if page_size < 1 or page_num < 1:
                return_payload = {
                    'notice_list': {},
                    'total_count': total_count,
                    'message': "page_size & page_num must be greater than 0"
                }
                return return_payload, 400

        res, code = self._db_control.get_list(find_key=ref, return_fields=return_fields, page_size=page_size,
                                              page_num=page_num)
        if code == 200:  # OK
            return_payload = {
                'user_list': res,
                'total_count': total_count
            }
            return return_payload, code
        elif code == 404:  # NOT FOUND
            return_payload = {
                'user_list': {},
                'total_count': total_count
            }
            return return_payload, code
        else:
            return total_count, code

    @self_logger_decorator  # returns auth token payload
    def _encode_token(self, user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=90),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        token = jwt.encode(payload, self._secret_key)
        return token, 200


class CustomerControlSingleton(CustomerControl, metaclass=Singleton):
    pass
