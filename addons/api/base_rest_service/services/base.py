import logging

log = logging.getLogger(__name__)

class ServiceMixin(object):
    def _serialize(self, record_id):
        return {}
    
    # Base Validators
    def _validator_search(self):
        return {}
    
    def _validator_get(self):
        return {}
    
    def _validator_return_get(self):
        return self._get_object_schema()
    
    # Base Validators
    def _validator_create(self):
        return {}

    def _validator_return_create(self):
        return self._get_object_schema()

    def _validator_update(self):
        return {}

    def _validator_return_update(self):
        return self._get_object_schema()

    def _validator_search(self):
        return {}

    def _validator_return_search(self):
        return {}

    def _validator_delete(self):
        return {}

    def _validator_return_delete(self):
        return self._get_object_schema()
    
    def _get(self, _id):
        return self.env[self._model].sudo().browse(_id)

    def _get_object_schema(self):
        return {}

    def _to_json(self, record_ids, many=False):
        if many:
            data = record_ids or []
            return {
                "results": [self._serialize(record_id) for record_id in data]
            }
            
        if not record_ids:
            return {}

        return self._serialize(record_ids)

class PaginatedServiceMixin(ServiceMixin):

    def _validator_search(self):
        return {
            "offset": {"type": "string", "required": False, "nullable": True},
            "limit": {"type": "string", "required": False, "nullable": True},
            "active": {"type": "string", "required": False, "nullable": True}
        }

    def _validator_return_search(self):
        schema = {
            "total_count": {"type": "integer", "required": False, "empty": False},
            "offset": {"type": "integer", "required": False, "empty": False},
            "limit": {"type": "integer", "required": False, "empty": False},
            "results": {
                "type": "list",
                "schema": {
                    "type": "dict",
                    "schema": self._get_object_schema()
                } 
            }
        }

        return schema

    def _to_json(self, record_ids, many=False, total_count=0, offset=0, limit=0):
        if many:
            data = record_ids or []
            return {
                "total_count": total_count,
                "offset": offset,
                "limit": limit,
                "results": [self._serialize(record_id) for record_id in data]
            }
            
        if not record_ids:
            return {}

        return self._serialize(record_ids)

