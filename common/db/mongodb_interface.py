import pymongo
from common.SingletonTemplate import Singleton
from common.PKLogger import PKLogger
from common.conf.ConfigControl import ConfigObj


class MongodbInterface:
    def __init__(self):
        config = ConfigObj()
        self._log = PKLogger('mongodb_interface', config.getSectionDict('log'))
        self._db_client = None
        self._db = None
        self._collect = None
        self._database = config.getValue('mongodb', 'database')
        # self._collection_name = config.getValue('mongodb', 'collection')
        self._user = config.getValue('mongodb', 'user')
        self._password = config.getValue('mongodb', 'password')
        self._host = config.getValue('mongodb', 'host')
        self._port = config.getValue('mongodb', 'port')

        self._my_collection = None

        self._log.info_json('init', {
            'database': self._database,
            # 'collection': self._collection_name,
            'user': self._user,
            'password': self._password,
            'host': self._host,
            'port': self._port
        })
        self.connection()
        print('xxxx')

    def connection(self):
        success = True
        try:
            self._db_client = pymongo.MongoClient(
                host=self._host,
                port=self._port,
                username=self._user,
                password=self._password)
            self._db = self._db_client.get_database(self._database)
            res = self._db.command('ping')
            print(res)

            # self._collect = db.get_collection(self._collection_name)
            self._log.info('mongodb connection success')
            return success
        except Exception as e:
            self._log.error_json('connection', {
                'db': self._database,
                'Exception': str(e)
            })
            raise
        # finally:
        #     self._db_client.close()
        #     self._collect = None
        #     success = False
        #     pass

    def get_collect(self, collection_name):
        return self._db.get_collection(collection_name)

    def close(self):
        self._log.info_json('close', {'event': 'ok'})
        self._db_client.close()

    def get_log_handle(self):
        return self._log


class DBConnectorSingleton(MongodbInterface, metaclass=Singleton):
    pass
