"""
Fast Xpan
~~~~~~~~~

一个轻量化、便于使用的百度网盘API库。

   快速开始：

   >>> from fastxpan import FxConfiguration, FxFileApi
   >>> file_api = FxFileApi(FxConfiguration(access_token="..."))
   >>> suc, data = file_api.ls("/apps/MyApp")
   >>> suc
   True
   >>> data
   ['Hello', 'World']

... or

"""
__version__ = "0.0.1"

from .common.error_messages import fxerr
from .common.configuration import FxConfiguration

from .api.fx_file_api import FxFileApi
from .common.structs import FxFile, FxFileMeta, FxImage
