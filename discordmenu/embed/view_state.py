from typing import Dict, Any, Optional


class ViewState:
    def __init__(self, original_author_id: int, menu_type: str, raw_query: str,
                 extra_state: Optional[Dict[str, Any]] = None):
        self.extra_state = extra_state or {}
        self.menu_type = menu_type
        self.original_author_id = original_author_id
        self.raw_query = raw_query

    def serialize(self) -> Dict[str, Any]:
        """
        This method should be overriden for more complex menus.
        """
        ret = {
            'raw_query': self.raw_query,
            'menu_type': self.menu_type,
            'original_author_id': self.original_author_id,
        }
        ret.update(self.extra_state)
        return ret

    @classmethod
    async def deserialize(cls, ims: dict) -> "ViewState":
        """
        This method should be overriden for more complex menus.
        """
        original_author_id = ims['original_author_id']
        menu_type = ims['menu_type']
        raw_query = ims.get('raw_query')
        return cls(original_author_id, menu_type, raw_query, extra_state=ims)
