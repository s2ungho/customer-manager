import toml
import os.path
from common.SingletonTemplate import Singleton


# util class
# class Empty:
#     pass
#
# def getValue(value):
#     # find value type
#     try:
#         evalValue = eval(value)
#         if type(evalValue) in [int, float, list, tuple, dict, str]:
#             return evalValue
#     except NameError:
#         pass
#     return value

class ConfigCtrl(object):
    def __init__(self):
        self._config = None

    def loadingConfigFile(self, configfile=None):
        if configfile is not None:
            file_path = os.getcwd() + '/' + configfile
            if os.path.exists(file_path):
                with open(file_path) as fd:
                    print(fd)
                    raw_config = fd.read()
                    self._config = toml.loads(raw_config)

    def getValue(self, section, option):
        return self._config[section][option]

    def getSectionDict(self, section) -> dict:
        return self._config[section]

    # def setValue(self, section, option, value):
    #     # set value
    #     if not self._config.has_section(section):
    #         self._config.add_section(section)
    #     self._config[section][option] = str(value)
    #
    #     # set internal method
    #     if not hasattr(self, section):
    #         setattr(self, section, Empty())
    #     current_section = getattr(self, section)
    #     setattr(current_section, option, value)
    #
    # def save(self):
    #     with open(self.filename, 'w') as configfile:
    #         self._config.write(configfile)
    #         print("Saved Config : " + self.filename)

    # def getFilename(self):
    #     return self.filename


class ConfigObj(ConfigCtrl, metaclass=Singleton):
    pass
