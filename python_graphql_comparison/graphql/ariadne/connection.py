from ariadne.contrib.relay import RelayConnection

from python_graphql_comparison.graphql.ariadne.utils import encode_cursor


class ObjectConnection(RelayConnection):
    def get_cursor(self, obj) -> str:
        obj_id = str(getattr(obj, self.id_field))
        return encode_cursor(obj_id)
