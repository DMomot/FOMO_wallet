from web3 import HTTPProvider
import json
from web3._utils.request import make_post_request


class MyHTTPProvider(HTTPProvider):
    def __init__(self, endpoint_uri=None, request_kwargs={"timeout": 60}, session=None):
        super().__init__(
            endpoint_uri=endpoint_uri,
            request_kwargs=request_kwargs,
            session=session,
        )

    def send(self, requests: list[dict]) -> list[dict]:
        request = json.dumps(requests).encode()
        raw_response = make_post_request(
            self.endpoint_uri, request, **self.get_request_kwargs(),
        )
        response = self.decode_rpc_response(raw_response)
        return response
