import json
from bson import ObjectId
from datetime import datetime, date


def json_encoder(o):
    if isinstance(o, (date, datetime)):
        return o.strftime("%Y-%m-%d %H:%M:%S.%f")
    elif isinstance(o, ObjectId):
        return str(o)


def json_dump(message):
    return json.dumps(message, ensure_ascii=False, default=json_encoder)  # ensure_ascii=False : 한글 Display를 위함

