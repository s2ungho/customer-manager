from werkzeug.security import generate_password_hash

def safety_set_property(input_dict, key, default=None, required=False):
    if key not in input_dict:
        if required:
            raise ValueError('invalid key error, {} is required'.format(key))
        else:
            return default
    return input_dict[key]

class UserProperty:
    def __init__(self, user_dict):
        # 필요한 필드만 초기화
        self._id = ""
        self.created_datetime = None
        self.updated_datetime = None
        self.customer_name = ""
        self.password_hash = ""
        self.phone = None
        self.address = None
        self.email = None
        self.membership_level = None
        self.marketing_level = False
        self.birth_date = None
        self.company = None
        self.comment = None
        self.set_property(user_dict)

    def set_property(self, user_dict):
        self._id = safety_set_property(user_dict, '_id', required=True)  # ObjectId 필수
        self.created_datetime = safety_set_property(user_dict, 'created_datetime', None)
        self.updated_datetime = safety_set_property(user_dict, 'updated_datetime', None)
        self.customer_name = safety_set_property(user_dict, 'customer_name', required=True)  # 필수 필드
        if 'password' in user_dict:
            self.password = safety_set_property(user_dict, 'password')
            self.password_hash = generate_password_hash(self.password)
        else:
            self.password_hash = safety_set_property(user_dict, 'password_hash', required=True)  # 필수 필드
        self.phone = safety_set_property(user_dict, 'phone', None)
        self.address = safety_set_property(user_dict, 'address', None)
        self.email = safety_set_property(user_dict, 'email', None)
        self.membership_level = safety_set_property(user_dict, 'membership_level', None)
        self.marketing_level = safety_set_property(user_dict, 'marketing_level', False)
        self.birth_date = safety_set_property(user_dict, 'birth_date', None)
        self.company = safety_set_property(user_dict, 'company', None)
        self.comment = safety_set_property(user_dict, 'comment', None)

    def get_user_property(self):
        # _id 필드를 제외한 나머지 필드를 반환
        member_property = {
            'created_datetime': self.created_datetime,
            'updated_datetime': self.updated_datetime,
            'customer_name': self.customer_name,
            'password_hash': self.password_hash,
            'phone': self.phone,
            'address': self.address,
            'email': self.email,
            'membership_level': self.membership_level,
            'marketing_level': self.marketing_level,
            'birth_date': self.birth_date,
            'company': self.company,
            'comment': self.comment
        }

        # 값이 None인 필드는 제거
        member_property = {k: v for k, v in member_property.items() if v is not None}
        return member_property

    def update_property(self, user_dict):
        # _id는 업데이트하지 않음
        self.customer_name = safety_set_property(user_dict, 'customer_name', self.customer_name)
        if 'password' in user_dict:
            self.password = safety_set_property(user_dict, 'password')
            self.password_hash = generate_password_hash(self.password)
        else:
            self.password_hash = safety_set_property(user_dict, 'password_hash', self.password_hash)
        self.phone = safety_set_property(user_dict, 'phone', self.phone)
        self.address = safety_set_property(user_dict, 'address', self.address)
        self.email = safety_set_property(user_dict, 'email', self.email)
        self.membership_level = safety_set_property(user_dict, 'membership_level', self.membership_level)
        self.marketing_level = safety_set_property(user_dict, 'marketing_level', self.marketing_level)
        self.birth_date = safety_set_property(user_dict, 'birth_date', self.birth_date)
        self.company = safety_set_property(user_dict, 'company', self.company)
        self.comment = safety_set_property(user_dict, 'comment', self.comment)

    # 다른 메서드는 동일하게 유지
    def get_user_id(self):
        return self._id

    def get_password(self):
        return self.password

    def get_token(self):
        return self.token

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active



    """def update_property(self, user_dict):
        self.user_name = safety_set_property(user_dict, 'user_name', self.user_name)
        if 'password' in user_dict:
            self.password = safety_set_property(user_dict, 'password')
            self.password_hash = generate_password_hash(self.password)
        self.email = safety_set_property(user_dict, 'email', self.email)
        self.phone = safety_set_property(user_dict, 'phone', self.phone)
        self.company = safety_set_property(user_dict, 'company', self.company)
        self.division = safety_set_property(user_dict, 'division', self.division)
        self.level = safety_set_property(user_dict, 'level', self.level)
        self.comment = safety_set_property(user_dict, 'comment', self.comment)
        self.is_receive_report = safety_set_property(user_dict, 'is_receive_report', self.is_receive_report)
        self.is_receive_alarm_email = safety_set_property(user_dict, 'is_receive_alarm_email',
                                                          self.is_receive_alarm_email)
        self.is_receive_alarm_sms = safety_set_property(user_dict, 'is_receive_alarm_sms', self.is_receive_alarm_sms)
        self.token = safety_set_property(user_dict, 'access_token', self.token)
        self.active = safety_set_property(user_dict, 'active', self.active)
        self.admin = safety_set_property(user_dict, 'is_admin', self.admin)
        self.favorite = safety_set_property(user_dict, 'favorite', self.favorite)

    def get_user_id(self):
        return self.user_id

    def get_password(self):
        return self.password

    def get_token(self):
        return self.token

    def is_admin(self):
        return self.admin

    def is_active(self):
        return self.active
"""