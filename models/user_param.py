from models.base_model import Model
from common import util


class UserParam(Model):
    def __init__(self,
                 active: bool = False,
                 login_datetime: str = None,
                 logout_datetime: str = None,
                 user_id: str = None,
                 user_name: str = None,
                 password_hash: str = None,
                 level: int = 0,
                 is_admin: bool = False,
                 email: str = None,
                 phone: str = None,
                 company: str = None,
                 division: str = None,
                 comment: str = None,
                 update_user: str = None,
                 is_receive_report: bool = False,
                 is_receive_alarm_email: bool = False,
                 is_receive_sms: bool = False):

        self.swagger_type = {
            'active': bool,
            'login_datetime': str,
            'logout_datetime': str,
            'user_id': str,
            'user_name': str,
            'password_hash': str,
            'level': int,
            'is_admin': bool,
            'email': str,
            'phone': str,
            'company': str,
            'division': str,
            'comment': str,
            'update_user': str,
            'is_receive_report': bool,
            'is_receive_alarm_email': bool,
            'is_receive_sms': bool
        }
        self.attribute_map = {
            'active': 'active',
            'login_datetime': 'login_datetime',
            'logout_datetime': 'logout_datetime',
            'user_id': 'user_id',
            'user_name': 'user_name',
            'password_hash': 'password_hash',
            'level': 'level',
            'is_admin': 'is_admin',
            'email': 'email',
            'phone': 'phone',
            'company': 'company',
            'division': 'division',
            'comment': 'comment',
            'update_user': 'update_user',
            'is_receive_report': 'is_receive_report',
            'is_receive_alarm_email': 'is_receive_alarm_email',
            'is_receive_sms': 'is_receive_sms'
        }

        self._active = active,
        self._login_datetime = login_datetime,
        self._logout_datetime = logout_datetime,
        self._user_id = user_id,
        self._user_name = user_name,
        self._password_hash = password_hash,
        self._level = level,
        self._is_admin = is_admin,
        self._email = email,
        self._phone = phone,
        self._company = company,
        self._division = division,
        self._comment = comment,
        self._update_user = update_user,
        self._is_receive_report = is_receive_report,
        self._is_receive_alarm_email = is_receive_alarm_email,
        self._is_receive_sms = is_receive_sms

    @classmethod
    def from_dict(cls, dikt) -> 'ioset_param':
        return util.deserialize_model(dikt, cls)

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, active: bool):
        self._active = active

    @property
    def login_datetime(self) -> str:
        return self._login_datetime

    @login_datetime.setter
    def login_datetime(self, login_datetime: str):
        self._login_datetime = login_datetime

    @property
    def logout_datetime(self) -> str:
        return self._logout_datetime

    @logout_datetime.setter
    def logout_datetime(self, logout_datetime: str):
        self._logout_datetime = logout_datetime

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, user_id: str):
        self._user_id = user_id

    @property
    def user_name(self) -> str:
        return self._user_name

    @user_name.setter
    def user_name(self, user_name: str):
        self._user_name = user_name

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password_hash: str):
        self._password_hash = password_hash

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, level: int):
        self._level = level

    @property
    def is_admin(self) -> bool:
        return self._is_admin

    @is_admin.setter
    def is_admin(self, is_admin: bool):
        self._is_admin = is_admin

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, phone: str):
        self._phone = phone

    @property
    def company(self) -> str:
        return self._company

    @company.setter
    def company(self, company: str):
        self._company = company

    @property
    def division(self) -> str:
        return self._division

    @division.setter
    def division(self, division: str):
        self._division = division

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str):
        self._comment = comment

    @property
    def update_user(self) -> str:
        return self._update_user

    @update_user.setter
    def update_user(self, update_user: str):
        self._update_user = update_user

    @property
    def is_receive_report(self) -> bool:
        return self._is_receive_report

    @is_receive_report.setter
    def is_receive_report(self, is_receive_report: bool):
        self._is_receive_report = is_receive_report

    @property
    def is_receive_alarm_email(self) -> bool:
        return self._is_receive_alarm_email

    @is_receive_alarm_email.setter
    def is_receive_alarm_email(self, is_receive_alarm_email: bool):
        self._is_receive_alarm_email = is_receive_alarm_email

    @property
    def is_receive_sms(self) -> bool:
        return self._is_receive_sms

    @is_receive_sms.setter
    def is_receive_sms(self, is_receive_sms: bool):
        self._is_receive_sms = is_receive_sms
