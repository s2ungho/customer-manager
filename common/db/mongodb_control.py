from pymongo import collection

from common.conf.ConfigControl import ConfigObj
from common.db.mongodb_interface import DBConnectorSingleton
from common.decorator import self_logger_decorator


class MongodbControl:
    def __init__(self, collection_name):
        db_connector = DBConnectorSingleton()
        self._collect = db_connector.get_collect(collection_name=collection_name)
        self._log = db_connector.get_log_handle()

    @self_logger_decorator
    def insert(self, body):
        assert body is not None
        doc = self._collect.insert_one(body)
        return str(doc.inserted_id), 200

    @self_logger_decorator
    def insert_many(self, body):
        assert body is not None
        doc = self._collect.insert_many(body)
        # res = list(map(str, doc.inserted_ids))
        return doc.inserted_ids, 200

    @self_logger_decorator
    def update(self, ref, set_body, return_field=None,upsert=False):
        assert ref is not None
        assert set_body is not None
        self._log.info_json(method='update', event='run',
                            raw_json={
                                'ref': ref,
                                'set_body': set_body,
                                'return_fields': return_field,
                            })

        doc = self._collect.find_one_and_update(ref, {'$set': set_body},
                                                upsert=upsert, return_document=collection.ReturnDocument.AFTER,
                                                projection=return_field)
        doc['_id'] = str(doc['_id'])
        return doc, 200

    @self_logger_decorator
    def update_query(self, ref, update_query, return_field=None, upsert=True):
        assert ref is not None
        assert update_query is not None
        self._log.info_json(method='update', event='run',
                            raw_json={
                                'ref': ref,
                                'set_body': update_query,
                                'return_fields': return_field,
                            })

        doc = self._collect.find_one_and_update(ref, update_query,
                                                upsert=upsert, return_document=collection.ReturnDocument.AFTER,
                                                projection=return_field)
        doc['_id'] = str(doc['_id'])
        return doc, 200

    @self_logger_decorator
    def update_many(self, ref, set_body, unset_body: dict = None):
        self._log.debug_json(method='update_many', event='run')
        _udpate_body = {}
        if set_body is not None:
            _udpate_body['$set'] = set_body
        if unset_body is not None:
            _udpate_body['$unset'] = unset_body
        doc = self._collect.update_many(filter=ref, update=_udpate_body, upsert=False)
        self._log.debug_json(method='update_many', event='run',
                             raw_json={
                                 'matched_count': doc.matched_count,
                                 'modified_count': doc.modified_count,
                                 'upserted_id': doc.upserted_id
                             })

        return doc.modified_count, 200

    @self_logger_decorator
    def get_list(self, find_key=None, return_fields=None, page_size=None, page_num=None):
        self._log.info_json(method='get_list', event='run',
                            raw_json={
                                'find_key': find_key,
                                'return_fields': return_fields,
                                'page_size': page_size,
                                'page_num': page_num
                            })
        if find_key is None:
            _filter = {}
        else:
            _filter = find_key
            # if '_id' in _filter:
            #     _filter['_id'] = ObjectId(_filter['_id'])
        if page_size is None:
            cursor = self._collect.find(filter=_filter, projection=return_fields)
        else:
            skips = page_size * (page_num - 1)
            cursor = self._collect.find(filter=_filter, projection=return_fields, skip=skips, limit=page_size)

        ret = []
        for doc in cursor:
            # print(doc)
            doc['_id'] = str(doc['_id'])
            ret.append(doc)
        # print(ret)
        if len(ret) == 0:
            return 'not found', 404

        return ret, 200

    @self_logger_decorator
    def count(self, fields=None):
        if fields is None:
            fields = {}
        ret = self._collect.count_documents(fields)
        if ret == 0:
            return 0, 404
        return ret, 200

    @self_logger_decorator
    def find_one(self, ref_info, return_fields=None, sort_key=None):
        assert ref_info is not None
        if sort_key is None:
            ret = self._collect.find_one(ref_info, return_fields)
        else:
            ret = self._collect.find_one(ref_info, return_fields, sort=[(sort_key, -1)])

        if ret is not None:
            ret['_id'] = str(ret['_id'])
        else:
            self._log.warning_json(method='find_one', event='run', message='not found')
            return {'message': 'not found'}, 404
        return ret, 200

    @self_logger_decorator
    def delete(self, ref):
        assert ref is not None
        self._log.debug_json('delete', {'ref': str(ref)})
        ret = self._collect.delete_one(ref)
        if ret.deleted_count == 0:
            self._log.warning_json(method='delete', event='run',
                                   message='can not delete',
                                   raw_json={
                                       'ref': ref,
                                   })
            return {'message': 'not found'}, 404
        else:
            self._log.info_json(method='delete', event='run',
                                raw_json={
                                    'delete count': ret.deleted_count,
                                })

        return ret.deleted_count, 204

    @self_logger_decorator
    def aggregate(self, pipeline):
        ret = self._collect.aggregate(pipeline)
        return ret, 200

    @self_logger_decorator
    def join(self, pipeline):
        doc = self._collect.aggregate(pipeline)
        ret = []
        for c in doc:
            ret.append(c)
        if len(ret) > 0:
            code = 200
        else:
            code = 404
        return ret, code

    @self_logger_decorator
    def distinct_many(self, filter_key, field_list):
        doc = self._collect.find(filter_key, field_list)
        prop_list = {}
        for item in field_list:
            res = doc.distinct(item)
            prop_list[item] = res
        return prop_list, 200

    @self_logger_decorator
    def distinct(self, field_list):
        doc = self._collect.distinct(field_list)
        return doc, 200

    @self_logger_decorator
    def find_and_distinct(self, distinct_key, find_key=None, return_fields=None):
        doc = self._collect.find(find_key, return_fields)
        ret = []
        if doc is not None:
            for i in doc:
                ret.append(i)

        if len(ret) == 0:
            return 'not found', 404
        print(ret)
        dist_list = doc.distinct(distinct_key)
        return dist_list, 200

    @self_logger_decorator
    def bulk_write(self, requests):
        result = self._collect.bulk_write(requests)
        return result, 200

    @self_logger_decorator
    def create_index(self, key_dict):
        result = self._collect.create_index(key_dict)
        return result, 200


if __name__ == '__main__':
    conf_file = '../../config_localtest.toml'

    config = ConfigObj()
    config.loadingConfigFile(conf_file)
    db_control = MongodbControl('item')
    ref = {
        'product_group': 'NCM'
    }
    print(db_control.get_list(ref, page_size=2, page_num=1))
