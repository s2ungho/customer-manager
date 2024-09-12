from common.PKLogger import PKLogger
from common.SingletonTemplate import Singleton
from common.conf.ConfigControl import ConfigObj

class MainLogger(object):
    def __init__(self):
        config = ConfigObj()
        self._Log = PKLogger('main', config.getSectionDict('log'))

    def logger(self):
        return self._Log


class MainLoggerSingleton(MainLogger, metaclass=Singleton):
    pass
