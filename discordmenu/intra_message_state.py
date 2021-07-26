import base64
import json
from typing import Dict, Optional, Any
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse, parse_qs

from discord import Embed

DEFAULT_QUERY_PARAM_KEYS = {
    'author': 'imsa',
    'image': 'imsi',
    'footer': 'imsf',
    'thumbnail': 'imst',
}


class IntraMessageState:
    @staticmethod
    def serialize(icon_url: str, json_dict: Any, query_param_key: str = 'imsf') -> str:
        raw_bytes = base64.b64encode(json.dumps(json_dict).encode())
        data = str(raw_bytes)[2:-1]

        params = {query_param_key: data}
        url_parts = list(urlparse(icon_url))

        query = dict(parse_qsl(url_parts[4]))
        query.update(params)

        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)

    @staticmethod
    def deserialize(url: str, query_param_key: str) -> Optional[Dict]:
        parsed_url = urlparse(url)
        query_params_dict = parse_qs(parsed_url.query)
        data = query_params_dict.get(query_param_key)
        if not data:
            return None

        result_bytes = base64.b64decode(data[0])
        return json.loads(result_bytes)

    @staticmethod
    def extract_data(embed: Embed, query_param_keys: Optional[Dict] = None) -> Dict:
        values_to_try = [
            ('author', embed.author.icon_url),
            ('image', embed.image.url),
            ('footer', embed.footer.icon_url),
            ('thumbnail', embed.thumbnail.url),
        ]

        if not query_param_keys:
            query_param_keys = DEFAULT_QUERY_PARAM_KEYS

        ret: Dict = {}
        for key, url in values_to_try:
            if not url:
                continue

            query_param_key = query_param_keys.get(key)
            data = IntraMessageState.deserialize(url, query_param_key)
            if data is None:
                # found url but not intra message state keys.
                continue

            IntraMessageState._merge_dicts(ret, data)
        return ret

    @staticmethod
    def _merge_dicts(target: Dict, data: Dict) -> None:
        for key, val in data.items():
            if key in target:
                existing_data = target[key]
                if not isinstance(existing_data, list):
                    # upgrade to vector
                    target[key] = [existing_data]
                target[key].append(val)
            else:
                target[key] = val
