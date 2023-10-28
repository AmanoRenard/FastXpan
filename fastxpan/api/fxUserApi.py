import xpan
from xpan import ApiException
from xpan.api import userinfo_api
from ..common.errors import fxerr
from ..common.configuration import FxConfiguration
from ..common.structs import FxUser, FxUserQuota


class FxUserApi:
    """百度网盘用户信息API

    初始化:

    >>> fx_conf = FxConfiguration(access_token="...")
    >>> user_api = FxUserApi(fx_conf)

    调用API:

    >>> err, data = user_api.get_user_quota()
    >>> if not err:
    >>>     print(data)
    {'baidu_name': '...', ...}

    Args:
        conf (FxConfiguration): access_token属性不能为空
    """

    def __init__(self, conf: FxConfiguration):
        self.access_token = conf.access_token

    def get_user_info(self) -> tuple[str | None, FxUser | None]:
        """获取当前用户信息

        Returns:
            tuple[str | None, FxUser | None]: 错误信息以及用户信息
        """
        with xpan.ApiClient() as api_client:
            api = userinfo_api.UserinfoApi(api_client)
            try:
                res = api.xpannasuinfo(access_token=self.access_token)
                if res["errno"] != 0:
                    return fxerr[res["errno"]], None
                return None, FxUser(res)
            except ApiException as e:
                return e.body, None

    def get_user_quota(self) -> tuple[str | None, FxUserQuota | None]:
        """获取当前用户网盘容量信息

        Returns:
            tuple[str | None, FxUserQuota | None]: 错误信息以及容量信息
        """
        with xpan.ApiClient() as api_client:
            api = userinfo_api.UserinfoApi(api_client)
            try:
                res = api.apiquota(access_token=self.access_token)
                if res["errno"] != 0:
                    return fxerr[res["errno"]], None
                return None, FxUserQuota(res)
            except ApiException as e:
                return e.body, None
