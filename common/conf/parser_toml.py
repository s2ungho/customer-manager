import toml
import os.path

def getConfigDict(configfile = None):
    configDict = None
    #file_path = os.getcwd() + configfile

    if configfile is not None:
        if os.path.exists(configfile):
            with open(configfile) as fd:
                raw_config = fd.read()
                log_config = toml.loads(raw_config)
            return log_config
    return None


