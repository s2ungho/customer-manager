from influxdb_client import InfluxDBClient, WriteOptions
from influxdb_client.client.write_api import ASYNCHRONOUS, WriteType

from common.conf.ConfigControl import ConfigObj
from common.mainlogger import PKLogger


class InfluxdbInterface:
    def __init__(self):
        config = ConfigObj()
        self._log = PKLogger('influxdb_interface', config.getSectionDict('log'))
        self._org = config.getValue('influxdb', 'organization')
        self._bucket = config.getValue('influxdb', 'bucket')
        self._token = config.getValue('influxdb', 'token')
        host = config.getValue('influxdb', 'host')
        port = config.getValue('influxdb', 'port')
        self._url = f"http://{host}:{port}"
        self._client = None
        self._write_api = None
        self._query_api = None

    def connection(self):
        connection_info = {
            'url': self._url,
            'org': self._org,
            'token': self._token,
        }
        try:
            self._client = InfluxDBClient(url=self._url, token=self._token, org=self._org)
            self._log.info_json('connection', 'run', message='Connect Success', raw_json=connection_info)
            self._write_api = self._client.write_api(write_options=WriteOptions(batch_size=500,
                                                                                flush_interval=10_000,
                                                                                jitter_interval=2_000,
                                                                                retry_interval=5_000,
                                                                                max_retries=5,
                                                                                max_retry_delay=30_000,
                                                                                exponential_base=2,
                                                                                write_type=WriteType.asynchronous))
            self._query_api = self._client.query_api()
        except Exception as e:
            self._log.critical_json('connection', 'exception', message=f"exception : {str(e)}",
                                    raw_json=connection_info)
            pass

    def ping(self):
        try:
            print("ping......")
            print(self._client.ping())
        except Exception as e:
            self._log.critical_json('ping', 'exception', message=f'exception : {str(e)}')

    def close(self):
        self._client.close()

    async def write_points(self, bucket, line_type_dataset):
        try:
            async_result = self._write_api.write(bucket=bucket, org=self._org, record=line_type_dataset)
            print(async_result.get())
            self._client.close()
        except Exception as e:
            self._log.critical_json('write_points', 'exception', message=f'exception : {str(e)}')
            raise

    def query(self, query_statement):
        try:
            res = self._query_api.query(query_statement)
            return res
        except Exception as e:
            self._log.critical_json('query', 'exception', message=f'exception : {str(e)}')
            raise
