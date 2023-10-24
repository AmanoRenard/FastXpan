import xpan
from xpan.api import userinfo_api
from ..common.configuration import FxConfiguration


class UserApi:
    """用户信息API
    """

    def __init__(self, configuration: FxConfiguration):
        self.access_token = configuration.access_token

    def user_quota(self):
        with xpan.ApiClient() as api_client:
            api = userinfo_api.UserinfoApi(api_client)
            try:
                return True, api.apiquota(self.access_token)
            except Exception as e:
                return False, e.__str__()
