import xpan
from xpan.api import auth_api as xpan_auth_api
from xpan.exceptions import ApiException
from urllib import parse

from ..common.configuration import FxConfiguration


class FxAuthApi:
    """百度网盘认证API

    初始化:

    >>> fx_conf = FxConfiguration(client_id="...", device_id="...", client_secret="...")
    >>> auth_api = FxAuthApi(fx_conf)

    调用API:

    >>> auth_api.get_code_url()
    'https://openapi.baidu.com/oauth/2.0/authorize?...'

    Args:
        conf (FxConfiguration): 需要初始化client_id、device_id、client_secret
    """

    def __init__(self, conf: FxConfiguration):
        self.client_id = conf.client_id
        self.device_id = conf.device_id
        self.client_secret = conf.client_secret

    def get_code_url(self) -> str:
        """获取用户授权地址

        Returns:
            str: 用户授权地址
        """
        query = {"response_type": "code",
                 "client_id": self.client_id,
                 "redirect_uri": "oob",
                 "scope": "basic,netdisk",
                 "device_id": self.device_id,
                 "display": "popup"}
        url = f"https://openapi.baidu.com/oauth/2.0/authorize?{parse.urlencode(query)}"
        return url

    def get_token(self, code: str) -> (bool, any):
        with xpan.ApiClient() as api_client:
            api = xpan_auth_api.AuthApi(api_client)
            try:
                return True, api.oauth_token_code2token(code, self.client_id, self.client_secret, "oob")
            except ApiException as e:
                return False, e.body

    def get_freshen_token(self, refresh_token: str) -> (bool, any):
        with xpan.ApiClient() as api_client:
            api = xpan_auth_api.AuthApi(api_client)
            try:
                return True, api.oauth_token_refresh_token(refresh_token, self.client_id, self.client_secret)
            except ApiException as e:
                return False, e.body
