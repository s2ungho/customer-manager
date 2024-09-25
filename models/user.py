from werkzeug.security import check_password_hash
from models.user_property import UserProperty


def safety_set_property(input_dict, key, var_type=str, required=False):
    if key not in input_dict:
        if required:
            raise ValueError('invalid key error, {} is required'.format(key))
        else:
            return None
    return var_type(input_dict[key])


class User(UserProperty):
    def __init__(self, user_dict):
        UserProperty.__init__(self, user_dict)

    def __repr__(self):
        r = self.get_user_property()
        return str(r)

    def to_dict(self):
        return self.get_user_property()

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def validate_token(self, token):
        return self.token == token

    def is_admin(self):
        return self.admin

    def get_password_hash(self):
        return self.password_hash
