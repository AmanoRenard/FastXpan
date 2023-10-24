from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Literal, Any
from urllib import parse
from hashlib import md5

import json
import requests
import xpan
from tqdm import tqdm
from xpan import ApiException
from xpan.api import fileinfo_api, multimediafile_api, filemanager_api, fileupload_api

from ..common.configuration import FxConfiguration
from ..common.structs import FxFile, FxFileMeta, FxImage
from ..common.error_messages import fxerr


class FxFileApi:
    """百度网盘文件操作API

    初始化:

    >>> fx_conf = FxConfiguration(access_token="...")
    >>> file_api = FxFileApi(fx_conf)

    调用API:

    >>> suc, data = file_api.ls("/apps/MyApp")
    >>> suc
    True
    >>> data
    ['Hello', 'World']

    Args:
        conf (FxConfiguration): access_token属性不能为空
    """

    def __init__(self, conf: FxConfiguration):
        if conf.access_token is ...:
            self.access_token = None
        else:
            self.access_token = conf.access_token

    def get_file_by_path(self, file_path: str = "/apps") -> (tuple[Literal[True], FxFile] |
                                                             tuple[Literal[False], str]):
        """通过路径获取单个文件、目录信息

        Args:
            file_path (str, optional): 文件或目录路径. 默认为 "/apps".

        Returns:
            (True, FxFile) | (False, str): (是否成功, 文件、目录信息 或 错误信息)
        """
        if file_path == "/":
            return False, "文件路径不能为根目录"
        if not file_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            fname = PurePosixPath(file_path).name.__str__()
            fpath = PurePosixPath(file_path).parent.__str__()
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=fpath)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                files = [FxFile(f) for f in res["list"] if f["server_filename"] == fname]
                if len(files) == 0:
                    return False, "文件不存在"
                else:
                    return True, files[0]
            except ApiException as e:
                return False, e.body

    def get_file_meta_by_path(self, file_path: str = "/apps") -> (tuple[Literal[True], FxFileMeta] |
                                                                  tuple[Literal[False], str]):
        """通过路径获取单个文件或目录的详细信息

        Args:
            file_path (str, optional): 文件或目录路径. 默认为 "/apps".

        Returns:
            (True, FxFileMeta) | (False, str): (是否成功, 文件、目录详细信息 或 错误信息)
        """
        if file_path == "/":
            return False, "文件路径不能为根目录"
        if not file_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            fname = PurePosixPath(file_path).name.__str__()
            fpath = PurePosixPath(file_path).parent.__str__()
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=fpath)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                files = [FxFileMeta(f) for f in res["list"] if f["server_filename"] == fname]
                if len(files) == 0:
                    return False, "文件不存在"
                else:
                    return True, files[0]
            except ApiException as e:
                return False, e.body

    def get_file_fsid_by_path(self, file_path: str = "/apps") -> tuple[Literal[True], int] | tuple[Literal[False], str]:
        """通过路径获取文件或目录的fsid

        Args:
            file_path (str, optional): 文件或目录路径. 默认为 "/apps".

        Returns:
            (True, int) | (False, str): (是否成功, 文件、目录的fs_id 或 错误信息)
        """
        if file_path == "/":
            return False, "文件路径不能为根目录"
        if not file_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            fname = PurePosixPath(file_path).name.__str__()
            fpath = PurePosixPath(file_path).parent.__str__()
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=fpath)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                files = [f["fs_id"] for f in res["list"] if
                         f["server_filename"] == fname]
                if len(files) == 0:
                    return False, "文件未找到"
                else:
                    return True, files[0]
            except ApiException as e:
                return False, e.body

    def list_files_by_path(self, dir_path: str = "/apps") -> (tuple[Literal[True], list[FxFile]] |
                                                              tuple[Literal[False], str]):
        """列出某个目录下的所有文件以及目录信息

        Args:
            dir_path (str, optional): 目录路径. 默认为 "/apps".

        Returns:
            (True, list[FxFile]) | (False, str): (是否成功, 文件以及目录信息列表 或 错误信息)
        """
        if not dir_path.startswith("/"):
            return False, "无效的路径"

        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=dir_path)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, [FxFile(f) for f in res["list"]]
            except ApiException as e:
                return False, json.loads(e.body)["errmsg"]

    def list_file_metas_by_path(self, dir_path: str = "/apps") -> (tuple[Literal[True], list[FxFileMeta]] |
                                                                   tuple[Literal[False], str]):
        """列出某个目录下所有文件以及目录的详细信息

        Args:
            dir_path (str, optional): 目录路径. 默认为 "/apps".

        Returns:
            (True, list[FileMeta]) | (False, str): (是否成功, 文件以及目录详细信息列表 或 错误信息)
        """
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=dir_path)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, [FxFileMeta(f) for f in res["list"]]
            except ApiException as e:
                return False, json.loads(e.body)["errmsg"]

    def list_file_paths_by_path(self, dir_path: str = "/apps") -> (tuple[Literal[True], list[str]] |
                                                                   tuple[Literal[False], str]):
        """列出某个目录下所有文件以及目录的路径

        Args:
            dir_path (str, optional): 目录路径. 默认为 "/apps".

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件以及目录路径列表 或 错误信息)
        """
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=dir_path)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, [f["path"] for f in res["list"]]
            except ApiException as e:
                return False, e.body

    def list_dir_paths_by_path(self, dir_path: str = "/apps") -> (tuple[Literal[True], list[str]] |
                                                                  tuple[Literal[False], str]):
        """列出某个目录下所有目录的路径

        Args:
            dir_path (str, optional): 目录路径. 默认为 "/apps".

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件以及目录路径列表 或 错误信息)
        """
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=dir_path, folder="1")
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, [f["path"] for f in res["list"]]
            except ApiException as e:
                return False, e.body

    def list_file_names_by_path(self, dir_path: str = "/apps") -> (tuple[Literal[True], list[str]] |
                                                                   tuple[Literal[False], str]):
        """列出某个目录下所有文件以及目录的名称

        Args:
            dir_path (str, optional): 目录路径. 默认为 "/apps".

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件以及目录的名称列表 或 错误信息)
        """
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                res = api.xpanfilelist(self.access_token, dir=dir_path)
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, [f["server_filename"] for f in res["list"]]
            except ApiException as e:
                return False, e.body

    def ls(self, dir_path: str = "/apps"):
        """列出所有文件以及目录的名称

        Args:
            dir_path (str, optional): 目录路径. 默认为 "/apps".

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件以及目录的名称列表 或 错误信息)
        """
        return self.list_file_names_by_path(dir_path)

    def list_file_paths_by_fsids(self, fs_ids: list[int]) -> (tuple[Literal[True], list[str]] |
                                                              tuple[Literal[False], str]):
        """根据fs_id列出文件以及目录的路径

        Args:
            fs_ids (list[int]): fs_id列表.

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件以及目录的路径列表 或 错误信息)
        """
        with xpan.ApiClient() as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            try:
                res = api.xpanmultimediafilemetas(self.access_token, fs_ids.__str__())
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, [f["path"] for f in res["list"]]
            except ApiException as e:
                return False, json.loads(e.body)["errmsg"]

    def get_file_path_by_fsid(self, fs_id: int) -> (tuple[Literal[True], list[str]] |
                                                    tuple[Literal[False], str]):
        """通过fs_id获取文件或目录的路径

        Args:
            fs_id (int): fs_id.

        Returns:
            (True, str) | (False, str): (是否成功, 文件以及目录的路径 或 错误信息)
        """
        with xpan.ApiClient() as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            try:
                res = api.xpanmultimediafilemetas(self.access_token, [fs_id].__str__())
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                res = [f["path"] for f in res["list"]]
                if not len(res):
                    return False, "无效的fs_id"
                return True, res[0]
            except ApiException as e:
                return False, json.loads(e.body)["errmsg"]

    def list_file_paths_by_search(self, key: str, dir_path: str = "/apps", recursion: bool = False) -> (
            tuple[Literal[True], list[str]] | tuple[Literal[False], str]):
        """根据关键字列出文件以及目录的路径

        Args:
            key (str): 关键字
            dir_path (str, optional): 搜索路径. 默认为 "/apps".
            recursion (bool, optional): 是否递归查找. 默认不递归.

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件以及目录详细信息列表 或 错误信息)
        """
        if key == "":
            return False, "关键字不能为空"
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                if recursion:
                    return True, [f["path"] for f in api.xpanfilesearch(self.access_token, key,
                                                                        dir=dir_path, recursion="1")["list"]]
                else:
                    return True, [f["path"] for f in api.xpanfilesearch(self.access_token, key,
                                                                        dir=dir_path)["list"]]
            except ApiException as e:
                return False, e.body

    def list_file_metas_by_search(self, key: str, dir_path: str = "/apps", recursion: bool = False) -> (
            tuple[Literal[True], list[FxFileMeta]] | tuple[Literal[False], str]):
        """根据关键字列出文件以及目录的详细信息

        Args:
            key (str): 关键字
            dir_path (str, optional): 搜索路径. 默认为 "/apps".
            recursion (bool, optional): 是否递归查找. 默认不递归.

        Returns:
            (True, list[FxFileMeta]) | (False, str): (是否成功, 文件以及目录详细信息列表 或 错误信息)
        """
        if key == "":
            return False, "关键字不能为空"
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                if recursion:
                    return True, [FxFileMeta(f) for f in api.xpanfilesearch(self.access_token, key,
                                                                            dir=dir_path, recursion="1")["list"]]
                else:
                    return True, [FxFileMeta(f) for f in api.xpanfilesearch(self.access_token, key,
                                                                            dir=dir_path)["list"]]
            except ApiException as e:
                return False, e.body

    def list_files_by_search(self, key: str, dir_path: str = "/apps", recursion: bool = False) -> (
            tuple[Literal[True], list[FxFile]] | tuple[Literal[False], str]):
        """根据关键字列出文件以及目录的信息

        Args:
            key (str): 关键字
            dir_path (str, optional): 搜索路径. 默认为 "/apps".
            recursion (bool, optional): 是否递归查找. 默认不递归.

        Returns:
            (True, list[FxFile]) | (False, str): (是否成功, 文件以及目录详细信息列表 或 错误信息)
        """
        if key == "":
            return False, "关键字不能为空"
        if not dir_path.startswith("/"):
            return False, "无效的路径"
        with xpan.ApiClient() as api_client:
            api = fileinfo_api.FileinfoApi(api_client)
            try:
                if recursion:
                    return True, [FxFile(f) for f in api.xpanfilesearch(
                        self.access_token, key, dir=dir_path, recursion="1")["list"]]
                else:
                    return True, [FxFile(f) for f in api.xpanfilesearch(
                        self.access_token, key, dir=dir_path)["list"]]
            except ApiException as e:
                return False, e.body

    def get_file_dlink_by_fsid(self, fs_id: int) -> tuple[bool, str]:
        """通过fs_id获取文件dlink

        Args:
            fs_id (str): 文件fs_id

        Returns:
            tuple[bool, str]: (是否成功, 文件的dlink或者错误信息)
        """
        with xpan.ApiClient() as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            try:
                res = api.xpanmultimediafilemetas(self.access_token, str([fs_id]), dlink="1")["list"]
                if not len(res):
                    return False, "无效的fs_id"
                if not res[0]["isdir"]:
                    return True, res[0]["dlink"]
                else:
                    return False, f"{res[0]['filename']} 不为文件"
            except IndexError:
                return False, "无效的fs_id"
            except ApiException as e:
                return False, e.body

    def get_file_dlink_by_path(self, file_path: str) -> tuple[bool, str]:
        """通过文件路径获取文件dlink

        Args:
            file_path (str): 文件路径

        Returns:
            tuple[bool, str]: (是否成功, 文件的dlink或者错误信息)
        """
        if file_path == "/":
            return False, "文件路径不能为根目录"
        if not file_path.startswith("/"):
            return False, "无效的路径"
        suc, data = self.get_file_fsid_by_path(file_path)
        if not suc:
            return suc, data
        return self.get_file_dlink_by_fsid(data)

    def list_file_dlinks_by_fsids(self, fs_ids: list[int]) -> (tuple[Literal[True], list[str]] |
                                                               tuple[Literal[False], str]):
        """通过fs_id列表获取列出多个dlink

        Args:
            fs_ids (List[str]): fs_id列表

        Returns:
            (True, list[str]) | (False, str): (是否成功, 文件的dlink或者错误信息)
        """
        with xpan.ApiClient() as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            try:
                return (True, [f["dlink"] for f in
                               api.xpanmultimediafilemetas(self.access_token, str(fs_ids), dlink="1")["list"] if
                               f["isdir"] == 0])
            except ApiException as e:
                return False, e.body

    @staticmethod
    def get_file_fsid_by_dlink(target_dlink: str) -> (tuple[Literal[True], int] |
                                                      tuple[Literal[False], str]):
        """通过dlink列表获取文件fs_id

                Args:
                    target_dlink (str): 目标dlink

                Returns:
                    (True, list[str]) | (False, str): (是否成功, 文件的fs_id或者错误信息)
                """
        if not target_dlink.__str__().startswith("https://d.pcs.baidu.com/file/"):
            return False, "无效的dlink"
        query = parse.parse_qs(parse.urlparse(target_dlink).query)
        if "fid" in query:
            return True, int(query["fid"][0][query["fid"][0].rindex("-") + 1:])
        return False, "无效的dlink"

    def list_images_by_path(self, target_dir_path):
        if target_dir_path == "/":
            return False, "文件路径不能为根目录"
        if not target_dir_path.startswith("/"):
            return False, "无效的路径"
        try:
            with xpan.ApiClient() as api_client:
                api = xpan.api.fileinfo_api.FileinfoApi(api_client)
                res = api.xpanfileimagelist(self.access_token, parent_path=target_dir_path, web="1")
                if res["errno"]:
                    return False, fxerr[res["errno"]]
                return True, [FxImage(f) for f in res["info"]]
        except ApiException as e:
            return False, e.body

    def get_file_name_by_fsid(self, fs_id: int) -> tuple[bool, str]:
        """通过fs_id获取文件或目录的名称

        Args:
            fs_id (int): 文件fs_id.

        Returns:
            tuple[bool, str]: (是否成功, 文件以及目录的名称 或 错误信息)
        """
        with xpan.ApiClient() as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            try:
                res = api.xpanmultimediafilemetas(self.access_token, [fs_id].__str__())
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                res = [f["filename"] for f in res["list"]]
                if not len(res):
                    return False, "无效的fs_id"
                return True, res[0]
            except ApiException as e:
                return False, json.loads(e.body)["errmsg"]

    def get_file_name_by_dlink(self, dlink: str) -> tuple[bool, str]:
        """通过dlink获取文件或目录的名称

        Args:
            dlink (int): 文件dlink.

        Returns:
            tuple[bool, str]: (是否成功, 文件以及目录的名称 或 错误信息)
        """
        suc, data = self.get_file_fsid_by_dlink(dlink)
        if not suc:
            return suc, data
        with xpan.ApiClient() as api_client:
            api = multimediafile_api.MultimediafileApi(api_client)
            try:
                res = api.xpanmultimediafilemetas(self.access_token, [data].__str__())
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                res = [f["filename"] for f in res["list"]]
                if not len(res):
                    return False, "无效的dlink"
                return True, res[0]
            except ApiException as e:
                return False, json.loads(e.body)["errmsg"]

    @staticmethod
    def __upload_check(local_file_path, target_dir_path, target_file_name, size):
        if target_dir_path == "/":
            return False, "文件路径不能为根目录"
        if not target_dir_path.startswith("/"):
            return False, "无效的路径"
        local_file_path = Path(local_file_path)
        if not local_file_path.is_file():
            return False, "文件不存在"
        total_size = local_file_path.stat().st_size
        if total_size > size:
            return False, "文件过大，请更换上传方式"
        if target_file_name is ...:
            return True, local_file_path.name, total_size
        return True, target_file_name, total_size

    def file_upload_mini(self, local_file_path: str, target_dir_path: str,
                         target_file_name: str = ..., overwrite: bool = False) -> tuple[bool, str]:
        """极简文件上传

        极简文件上传方法，速度最快，不支持断点续传，无进度条，适用于上传配置文件或小型文件。

        调用此方法上传文件的大小限制在2MB以内。

        百度网盘API只允许将文件上传到AccessToken对应的应用目录中，如"/apps/我的应用"，上传文件时会递归创建目录。

        Args:
            local_file_path (str): 本地文件路径
            target_dir_path (str): 目标目录路径
            target_file_name (str): 目标文件名，不填则为原文件名
            overwrite (bool, optional): 是否覆盖，默认为False

        Returns:
            tuple[bool, str]: (是否成功, 上传信息)

        """
        suc, target_file_name, total_size = self.__upload_check(
            local_file_path, target_dir_path, target_file_name, 2097152)
        if not suc:
            return False, target_file_name
        url = (f"https://d.pcs.baidu.com/rest/2.0/pcs/file?method=upload&access_token={self.access_token}&"
               f"path={parse.quote((PurePosixPath(target_dir_path) / target_file_name).__str__(), encoding='utf-8')}&"
               f"ondup={'overwrite' if overwrite else 'fail'}")
        with open(local_file_path, "rb") as upload_file:
            headers = {'User-Agent': 'pan.baidu.com'}
            res = requests.post(url, files={'file': upload_file}, headers=headers, timeout=30)
            if res.status_code != 200:
                return False, fxerr[json.loads(res.content.decode("utf-8"))["error_code"]]
            return True, "文件上传成功"

    def file_upload_simple(self, local_file_path: str, target_dir_path: str,
                           target_file_name: str = ..., overwrite: bool = False) -> tuple[bool, str]:
        """简单文件上传

        简单文件上传方法，不支持断点续传，适用于上传小型文件，由于网络波动，文件越大越容易失败。
        调用此方法上传时建议上传文件的大小在3MB以内，上传的文件大小如果超过4MB则自动返回失败。

        百度网盘API只允许将文件上传到AccessToken对应的应用目录中，如"/apps/我的应用"，上传文件时会递归创建目录。

        Args:
            local_file_path (str): 本地文件路径
            target_dir_path (str): 目标目录路径
            target_file_name (str): 目标文件名，不填则为原文件名
            overwrite (bool, optional): 是否覆盖，默认为False

        Returns:
            tuple[bool, str]: (是否成功, 上传信息)

        """
        suc, target_file_name, total_size = self.__upload_check(
            local_file_path, target_dir_path, target_file_name, 4194304)
        if not suc:
            return False, target_file_name
        url = (f"https://d.pcs.baidu.com/rest/2.0/pcs/file?method=upload&access_token={self.access_token}&"
               f"path={parse.quote((PurePosixPath(target_dir_path) / target_file_name).__str__(), encoding='utf-8')}&"
               f"ondup={'overwrite' if overwrite else 'fail'}")
        with open(local_file_path, "rb") as file:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                      desc=f"上传: {local_file_path.name}") as pbar:
                def file_gen():
                    for chunk in iter(lambda: file.read(1024), b''):
                        pbar.update(len(chunk))
                        yield chunk

                headers = {'User-Agent': 'pan.baidu.com'}
                res = requests.post(url, data=file_gen(), headers=headers, timeout=30)
                if res.status_code != 200:
                    return False, fxerr[json.loads(res.content.decode("utf-8"))["error_code"]]
                return True, "文件上传成功"

    def file_upload_multipart(self, local_file_path: str, target_dir_path: str, target_file_name: str = ...,
                              overwrite: bool = False, user_type: int = 0) -> tuple[bool, str]:
        """文件分片上传

        文件分片上传方法，可传较大文件。
        文件分片上传分为三个阶段：预上传、分片上传、创建文件。
        串行完成这三个阶段任务后，本地文件成功上传到网盘服务器。

        授权用户为普通用户时，单个分片大小固定为4MB，单文件总大小上限为4GB；
        授权用户为普通会员时，单个分片大小上限为16MB，单文件总大小上限为10GB；
        授权用户为超级会员时，用户单个分片大小上限为32MB，单文件总大小上限为20GB。

        百度网盘API只允许将文件上传到AccessToken对应的应用目录中，如"/apps/我的应用"，上传文件时会递归创建目录。

        Args:
            local_file_path (str): 本地文件路径
            target_dir_path (str): 目标目录路径
            target_file_name (str): 目标文件名，不填则为原文件名
            overwrite (bool, optional): 文件重名时是否覆盖
            user_type (int, optional): 用户类型，0普通用户、1普通会员、2超级会员，默认为普通用户

        Returns:
            tuple[bool, str]: (是否成功, 上传信息)

        """
        if target_dir_path == "/":
            return False, "文件路径不能为根目录"
        if not target_dir_path.startswith("/"):
            return False, "无效的路径"
        if user_type == 1:
            part_size = 16777216
            max_size = 10737418240
            iter_count = 16384
        else:
            if user_type == 2:
                part_size = 33554432
                max_size = 21474836480
                iter_count = 32768
            else:
                part_size = 4194304
                max_size = 4294967296
                iter_count = 4096
        local_file_path = Path(local_file_path)
        if not local_file_path.is_file():
            return False, "文件不存在"
        total_size = local_file_path.stat().st_size
        if not total_size:
            return False, "分片上传禁止上传空文件"
        if total_size > max_size:
            return False, "文件过大"
        if target_file_name is ...:
            target_file_name = local_file_path.name
        target_file_path = (PurePosixPath(target_dir_path) / target_file_name).__str__()
        if not overwrite and self.get_file_by_path(target_file_path)[0]:
            return False, "文件已存在"

        block_list = []
        with open(local_file_path, "rb") as file:
            with tqdm(total=total_size, unit='B', unit_scale=True,
                      desc=f"预上传: {local_file_path.name}") as pbar:
                i = 0
                _md5 = md5()
                for chunk in iter(lambda: file.read(1024), b''):
                    pbar.update(len(chunk))
                    if i < iter_count:
                        _md5.update(chunk)
                        i += 1
                    else:
                        block_list.append(_md5.hexdigest())
                        _md5 = md5(chunk)
                        i = 1
                if i:
                    block_list.append(_md5.hexdigest())
        block_list = json.dumps(block_list)

        with xpan.ApiClient() as api_client:
            api = fileupload_api.FileuploadApi(api_client)
            try:
                res = api.xpanfileprecreate(
                    self.access_token, target_file_path, 0, total_size, 1, block_list,
                    rtype=3 if overwrite else 0)
            except ApiException as e:
                return False, f"预上传失败: {e.body}"
            if res["errno"] != 0:
                return False, f"预上传失败: {fxerr[res['errno']]}"
            upload_id = res["uploadid"]
            block_list_index = res["block_list"]
            upload_file_tmp = Path(f"{local_file_path.__str__()}_FastXpanUpload_tmp")

            with open(local_file_path, "rb") as file:
                with tqdm(total=total_size, unit='B', unit_scale=True,
                          desc=f"上传: {local_file_path.name}") as pbar:
                    for part_seq in block_list_index:
                        with open(upload_file_tmp, "wb") as upload_part:
                            j = 0
                            for _chunk in iter(lambda: file.read(1024), b''):
                                upload_part.write(_chunk)
                                j += 1
                                if j >= iter_count:
                                    break
                            upload_part.close()
                        with open(upload_file_tmp, "rb") as upload_part:
                            if part_seq == len(block_list_index) - 1:
                                pbar.update(total_size - part_size * part_seq)
                            else:
                                pbar.update(part_size)
                            try:
                                res = api.pcssuperfile2(
                                    self.access_token, part_seq.__str__(), target_file_path, upload_id,
                                    type="tmpfile", file=upload_part)
                                if "errno" in res:
                                    return False, res
                            except ApiException as e:
                                return False, f"上传分片{part_seq}失败: {e.body}"
                            finally:
                                upload_part.close()
                                upload_file_tmp.unlink()

            try:
                res = api.xpanfilecreate(
                    self.access_token, target_file_path, 0, total_size, upload_id, block_list,
                    rtype=3 if overwrite else 0)
                if res["errno"]:
                    return False, fxerr[res["errno"]]
                return True, fxerr[res["errno"]]
            except ApiException as e:
                return False, f"创建文件{local_file_path.name}失败: {e.body}"

    def __file_download_by_dlink_simple(self, target_dlink: str, local_file_path: str,
                                        enable_error_log: bool) -> tuple[bool, str]:
        if not target_dlink.__str__().startswith("https://d.pcs.baidu.com/file/"):
            return False, "无效的dlink"
        url = f"{target_dlink}&access_token={self.access_token}"
        headers = {'User-Agent': 'pan.baidu.com'}
        local_file_path = Path(local_file_path + "_fxtmp")
        res = requests.get(url, headers=headers, stream=True, timeout=30)
        if res.status_code != 200:
            if enable_error_log:
                with open(local_file_path.__str__() + "_FastXpanErrorLog.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().__str__()}: {res.status_code} {json.loads(res.content)}\n")
            err_content = json.loads(res.content.decode("utf-8"))
            if err_content["error_code"] in fxerr:
                return False, fxerr[err_content["error_code"]]
            else:
                return False, err_content["error_msg"]
        total_size = int(res.headers["Content-Length"])
        try:
            with open(local_file_path, "wb") as file:
                with tqdm(total=total_size, unit='B', unit_scale=True,
                          desc="下载：" + local_file_path.name[:-6]) as pbar:
                    for chunk in res.iter_content(1024):
                        file.write(chunk)
                        pbar.update(len(chunk))
            local_file_path.rename(local_file_path.absolute().__str__()[:-6])
            return True, "下载完成"
        except ApiException as e:
            if enable_error_log:
                with open(local_file_path.__str__()[:-6] + "_FastXpanErrorLog.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().__str__()}: {e.__str__()}\n")
            local_file_path.unlink()
            return False, e.__str__()

    @staticmethod
    def __breakpoint_init(local_file_path, headers, url, enable_error_log):
        if local_file_path.is_file():
            first_byte = local_file_path.stat().st_size
        else:
            first_byte = 0
        if first_byte != 0:
            headers['Range'] = f"bytes={first_byte}-"
        try:
            res = requests.get(url, headers=headers, stream=True, timeout=30)
        except Exception as e:
            return False, e.__str__()
        if res.status_code not in [200, 206]:
            if enable_error_log:
                with open(local_file_path.__str__()[:-6] + "_FastXpanErrorLog.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().__str__()}: {res.status_code} {json.loads(res.content)}\n")
            err_content = json.loads(res.content.decode("utf-8"))
            if err_content["error_code"] in fxerr:
                return False, fxerr[err_content["error_code"]]
            else:
                return False, err_content["error_msg"]
        total_size = int(res.headers.get("Content-Length", 0))
        return True, (res, first_byte, total_size)

    def __file_download_by_dlink_breakpoint(self, target_dlink: str, local_file_path: str,
                                            enable_error_log: bool) -> tuple[bool, str]:
        if not target_dlink.__str__().startswith("https://d.pcs.baidu.com/file/"):
            return False, "无效的dlink"
        url = f"{target_dlink}&access_token={self.access_token}"
        headers = {'User-Agent': 'pan.baidu.com'}
        local_file_path = Path(local_file_path + "_fxtmp")
        suc, data = self.__breakpoint_init(local_file_path, headers, url, enable_error_log)
        if not suc:
            return False, data
        res, first_byte, total_size = data
        try:
            with open(local_file_path, "ab" if first_byte else "wb") as file:
                with tqdm(total=first_byte + total_size, unit='B', unit_scale=True,
                          desc="下载：" + local_file_path.name[:-6], initial=first_byte) as pbar:
                    for chunk in res.iter_content(1024):
                        file.write(chunk)
                        pbar.update(len(chunk))
            local_file_path.rename(local_file_path.absolute().__str__()[:-6])
            return True, "下载完成"
        except ApiException as e:
            if enable_error_log:
                with open(local_file_path.__str__()[:-6] + "_FastXpanErrorLog.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().__str__()}: {e.__str__()}\n")
            return False, e.__str__()

    def __file_download_by_dlink_breakpoint_auto_retry(
            self, target_dlink: str, local_file_path: str, max_retry: int = 3, enable_error_log: bool = False
    ) -> tuple[bool, str]:
        err = "Error"
        url = f"{target_dlink}&access_token={self.access_token}"
        headers = {'User-Agent': 'pan.baidu.com'}
        local_file_path = Path(local_file_path + "_fxtmp")
        for i in range(max_retry):
            try:
                if local_file_path.is_file():
                    first_byte = local_file_path.stat().st_size
                else:
                    first_byte = 0
                if first_byte != 0:
                    headers['Range'] = f"bytes={first_byte}-"
                res = requests.get(url, headers=headers, stream=True, timeout=30)
                if res.status_code not in [200, 206]:
                    if enable_error_log:
                        with open(local_file_path.__str__()[:-6] + "_FastXpanErrorLog.txt", "a", encoding="utf-8") as f:
                            f.write(f"{datetime.now().__str__()}: {res.status_code} {json.loads(res.content)}\n")
                    return False, fxerr[json.loads(res.content.decode("utf-8"))["error_code"]]
                total_size = int(res.headers.get("Content-Length", 0))
                with open(local_file_path, "ab" if first_byte else "wb") as file:
                    with tqdm(total=first_byte + total_size, unit='B', unit_scale=True,
                              desc="下载：" if not i else "重新下载：" + local_file_path.name[:-6],
                              initial=first_byte) as pbar:
                        for chunk in res.iter_content(1024):
                            file.write(chunk)
                            pbar.update(len(chunk))
                local_file_path.rename(local_file_path.absolute().__str__()[:-6])
                return True, "下载完成"
            except ApiException as e:
                if enable_error_log:
                    with open(local_file_path.__str__()[:-6] + "_FastXpanErrorLog.txt", "a", encoding="utf-8") as f:
                        f.write(f"{datetime.now().__str__()}: retry{i} {e.__str__()}\n")
                err = e.__str__()
        return False, err

    def __file_download_check(self, local_file_path: Path, overwrite: bool, what: int, what_data) -> tuple[bool, str]:
        if not local_file_path.parent.exists():
            return False, "文件保存路径错误"
        if local_file_path.is_file():
            if overwrite:
                local_file_path.unlink()
            else:
                return False, "文件已存在"
        d_link = "succeed"
        if what == 1:
            suc, d_link = self.get_file_dlink_by_fsid(what_data)
            if not suc:
                return suc, d_link
        if what == 2:
            suc, data = self.get_file_fsid_by_path(what_data)
            if not suc:
                return suc, data
            suc, d_link = self.get_file_dlink_by_fsid(data)
            if not suc:
                return suc, d_link
        return True, d_link

    def file_download_mini(self, target_file_path: str, local_dir_path: str,
                           local_file_name: str = ..., overwrite: bool = False):
        """极简文件下载

        极简文件下载方法，不带进度条，适用于下载配置文件和小型文件。

        Args:
            target_file_path (str): 需要下载的文件路径
            local_dir_path (str): 保存到的本地目录路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)

        Returns:
            tuple[bool, str]: (是否成功, 下载消息)
        """
        local_file_path = Path(local_dir_path) / (local_file_name
                                                  if not local_file_name else Path(target_file_path).name)
        suc, d_link = self.__file_download_check(local_file_path, overwrite, 2, target_file_path)
        if not suc:
            return suc, d_link
        if not d_link.__str__().startswith("https://d.pcs.baidu.com/file/"):
            return False, "无效的dlink"
        url = f"{d_link}&access_token={self.access_token}"
        headers = {'User-Agent': 'pan.baidu.com'}
        res = requests.get(url, headers=headers, stream=True, timeout=30)
        if res.status_code != 200:
            err_content = json.loads(res.content.decode("utf-8"))
            if err_content["error_code"] in fxerr:
                return False, fxerr[err_content["error_code"]]
            else:
                return False, err_content["error_msg"]
        try:
            with open(local_file_path, "wb") as file:
                for chunk in res.iter_content(1024):
                    file.write(chunk)
            return True, "下载完成"
        except ApiException as e:
            return False, e.body

    def __download_method(self, data, local_dir_path: str, local_file_name: str, overwrite: bool, method: int):
        if method == 0:
            suc, download_file_name = self.get_file_name_by_dlink(data)
            if not suc:
                return suc, download_file_name
            local_file_path = Path(local_dir_path) / (local_file_name if not local_file_name else download_file_name)
            suc, data = self.__file_download_check(local_file_path, overwrite, 0, None)
            if not suc:
                return suc, data
            return True, data, local_file_path
        else:
            if method == 1:
                suc, download_file_name = self.get_file_name_by_fsid(data)
                if not suc:
                    return suc, download_file_name
                local_file_path = Path(local_dir_path) / (
                    local_file_name if not local_file_name else download_file_name)
                suc, d_link = self.__file_download_check(local_file_path, overwrite, 1, data)
                if not suc:
                    return suc, d_link
                return suc, d_link, local_file_path
            else:
                local_file_path = Path(local_dir_path) / (local_file_name
                                                          if not local_file_name else Path(data).name)
                suc, d_link = self.__file_download_check(local_file_path, overwrite, 2, data)
                if not suc:
                    return suc, d_link
                return suc, d_link, local_file_path

    def file_download_simple_by_dlink(self, target_dlink: str, local_dir_path: str, local_file_name: str = ...,
                                      overwrite: bool = False, enable_error_log: bool = False):
        """简单文件下载(dlink)

        简单文件下载方法，不支持断点续传，适用于下载中小型文件，由于网络波动，文件越大越容易下载失败。
        调用此方法下载文件时建议文件的大小在50MB以内。

        下载文件时会产生一个后缀为_fxtmp的缓存文件，下载结束后自动移除，下载时程序非正常退出不会移除。

        Args:
            target_dlink (str): 需要下载的文件dlink
            local_dir_path (str): 保存到的本地文件路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)
            enable_error_log (bool, optional): 是否启用错误日志(默认为False)

        Returns:
            tuple[bool, str]: (是否成功, 下载消息)
        """
        suc, data, local_file_path = self.__download_method(
            target_dlink, local_dir_path, local_file_name, overwrite, 0)
        if not suc:
            return suc, data
        return self.__file_download_by_dlink_simple(target_dlink, local_file_path.__str__(), enable_error_log)

    def file_download_simple_by_fsid(self, target_file_fs_id: int, local_dir_path: str, local_file_name: str = ...,
                                     overwrite: bool = False, enable_error_log: bool = False) -> tuple[bool, str]:
        """简单文件下载(fs_id)

        简单文件下载方法，不支持断点续传，适用于下载中小型文件，由于网络波动，文件越大越容易下载失败。
        调用此方法下载文件时建议文件的大小在50MB以内。

        下载文件时会产生一个后缀为_fxtmp的缓存文件，下载结束后自动移除，下载时程序非正常退出不会移除。

        Args:
            target_file_fs_id (int): 需要下载的文件fs_id
            local_dir_path (str): 保存到的本地文件路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)
            enable_error_log (bool, optional): 是否启用错误日志(默认为False)

        Returns:
            tuple[bool, str]: (是否成功, 下载消息)
        """
        suc, d_link, local_file_path = self.__download_method(
            target_file_fs_id, local_dir_path, local_file_name, overwrite, 1)
        if not suc:
            return suc, d_link
        return self.__file_download_by_dlink_simple(d_link, local_file_path.__str__(), enable_error_log)

    def file_download_simple_by_path(self, target_file_path: str, local_dir_path: str, local_file_name: str = ...,
                                     overwrite: bool = False, enable_error_log: bool = False):
        """简单文件下载(file_path)

        简单文件下载方法，不支持断点续传，适用于下载中小型文件，由于网络波动，文件越大越容易下载失败。
        调用此方法下载文件时建议文件的大小在50MB以内。

        下载文件时会产生一个后缀为_fxtmp的缓存文件，下载结束后自动移除，下载时程序非正常退出不会移除。

        Args:
            target_file_path (str): 需要下载的文件路径
            local_dir_path (str): 保存到的本地文件路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)
            enable_error_log (bool, optional): 是否启用错误日志(默认为False)

        Returns:
            tuple[bool, str]: (是否成功, 下载消息)
        """
        suc, d_link, local_file_path = self.__download_method(
            target_file_path, local_dir_path, local_file_name, overwrite, 2)
        if not suc:
            return suc, d_link
        return self.__file_download_by_dlink_simple(d_link, local_file_path.__str__(), enable_error_log)

    def file_download_breakpoint_by_dlink(self, target_dlink: str, local_dir_path: str, local_file_name: str = ...,
                                          overwrite: bool = False, enable_error_log: bool = False,
                                          auto_retry: bool = True, max_retry: int = 3):
        """文件断点下载(dlink)

        文件断点下载方法，文件下载失败前的内容将保留，可以继续下载，适用于下载中型文件以及较大文件。

        下载文件时会产生一个后缀为_fxtmp的缓存文件，下载成功后自动移除。

        Args:
            target_dlink (str): 需要下载的文件dlink
            local_dir_path (str): 保存到的本地文件路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)
            enable_error_log (bool, optional): 是否启用错误日志(默认为False)
            auto_retry (bool, optional): 文件下载失败后是否重试(默认为True)
            max_retry (int, optional): 文件下载失败后的重试次数(默认为3)

        Returns:
            tuple[bool, str]: (是否成功, 下载消息)
        """
        suc, data, local_file_path = self.__download_method(
            target_dlink, local_dir_path, local_file_name, overwrite, 0)
        if not suc:
            return suc, data
        if auto_retry:
            return self.__file_download_by_dlink_breakpoint_auto_retry(
                target_dlink, local_file_path.__str__(), max_retry, enable_error_log)
        return self.__file_download_by_dlink_breakpoint(target_dlink, local_file_path.__str__(), enable_error_log)

    def file_download_breakpoint_by_fsid(self, target_file_fs_id: int, local_dir_path: str, local_file_name: str = ...,
                                         overwrite: bool = False, enable_error_log: bool = False,
                                         auto_retry: bool = True, max_retry: int = 3) -> tuple[bool, str]:
        """文件断点下载(fs_id)

        文件断点下载方法，文件下载失败前的内容将保留，可以继续下载，适用于下载中型文件以及较大文件。

        下载文件时会产生一个后缀为_fxtmp的缓存文件，下载成功后自动移除。

        Args:
            target_file_fs_id (int): 需要下载的文件fs_id
            local_dir_path (str): 保存到的本地文件路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)
            enable_error_log (bool, optional): 是否启用错误日志(默认为False)
            auto_retry (bool, optional): 文件下载失败后是否重试(默认为True)
            max_retry (int, optional): 文件下载失败后的重试次数(默认为3)

        Returns:
            tuple[bool, str]: (是否成功, 下载消息)
        """
        suc, d_link, local_file_path = self.__download_method(
            target_file_fs_id, local_dir_path, local_file_name, overwrite, 1)
        if not suc:
            return suc, d_link
        if auto_retry:
            return self.__file_download_by_dlink_breakpoint_auto_retry(
                d_link, local_file_path.__str__(), max_retry, enable_error_log)
        return self.__file_download_by_dlink_breakpoint(d_link, local_file_path.__str__(), enable_error_log)

    def file_download_breakpoint_by_path(self, target_file_path: str, local_dir_path: str, local_file_name: str = ...,
                                         overwrite: bool = False, enable_error_log: bool = False,
                                         auto_retry: bool = True, max_retry: int = 3):
        """文件断点下载(file_path)

        文件断点下载方法，文件下载失败前的内容将保留，可以继续下载，适用于下载中型文件以及较大文件。

        下载文件时会产生一个后缀为_fxtmp的缓存文件，下载成功后自动移除。

        Args:
            target_file_path (str): 需要下载的文件路径
            local_dir_path (str): 保存到的本地文件路径
            local_file_name (str, optional): 保存的文件名(默认为目标文件名)
            overwrite (bool, optional): 本地文件重名时是否覆盖(默认为False)
            enable_error_log (bool, optional): 是否启用错误日志(默认为False)
            auto_retry (bool, optional): 文件下载失败后是否重试(默认为True)
            max_retry (int, optional): 文件下载失败后的重试次数(默认为3)

        Returns:
            tuple[bool, str]: (是否成功, 下载信息)
        """
        suc, d_link, local_file_path = self.__download_method(
            target_file_path, local_dir_path, local_file_name, overwrite, 2)
        if not suc:
            return suc, d_link
        if auto_retry:
            return self.__file_download_by_dlink_breakpoint_auto_retry(
                d_link, local_file_path.__str__(), max_retry, enable_error_log)
        return self.__file_download_by_dlink_breakpoint(d_link, local_file_path.__str__(), enable_error_log)

    def files_delete_by_paths(self, target_dir_paths: list[str]):
        """删除多个文件

        Args:
            target_dir_paths (list[str]): 目标文件夹路径列表

        Returns:
            tuple[bool, Any] | tuple[bool, str]: 是否成功以及操作信息
        """
        with xpan.ApiClient() as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            try:
                res = api.filemanagerdelete(self.access_token, 1, json.dumps(target_dir_paths))
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, "操作成功"
            except ApiException as e:
                return False, e.body

    def file_delete_by_path(self, target_dir_path: str):
        """删除文件

        Args:
            target_dir_path (str): 目标文件夹路径

        Returns:
            tuple[bool, Any] | tuple[bool, str]: 是否成功以及操作信息
        """
        with xpan.ApiClient() as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            try:
                res = api.filemanagerdelete(self.access_token, 1, json.dumps([target_dir_path]))
                if res["errno"] != 0:
                    return False, fxerr[res["errno"]]
                return True, "操作成功"
            except ApiException as e:
                return False, e.body

    def mkdir(self, target_dir_path: str, rtype: int = 0) -> tuple[Literal[True], Any] | tuple[Literal[False], str]:
        """创建文件夹

        Args:
            target_dir_path (str): 目标文件夹路径
            rtype (int, optional): 文件命名策略，默认0。0 为不重命名，返回冲突，1 为只要path冲突即重命名。

        Returns:
            tuple[Literal[True], Any] | tuple[Literal[False], str]: 是否成功以及操作信息
        """
        url = f"https://pan.baidu.com/rest/2.0/xpan/file?method=create&access_token={self.access_token}"
        payload = {'path': target_dir_path,
                   'rtype': f'{rtype}',
                   'isdir': '1'}
        try:
            res = json.loads(requests.request("POST", url, data=payload).text)
            if res["errno"] != 0:
                return False, fxerr[res["errno"]]
            return True, fxerr[res["errno"]]
        except ApiException as e:
            return False, e.body

    def file_rename(self, file_path: str, new_name: str) -> tuple[bool, str]:
        """文件重命名

        Args:
            file_path (str): 文件路径
            new_name (str): 重命名

        Returns:
            tuple[bool, str] (是否成功, 操作信息)

        """
        with xpan.ApiClient() as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            try:
                res = api.filemanagerrename(self.access_token, 1,
                                            json.dumps([{"path": file_path, "newname": new_name}]))
                if res["info"][0]["errno"] != 0:
                    return False, fxerr[res["info"][0]["errno"]]
                return True, fxerr[res["info"][0]["errno"]]
            except ApiException as e:
                return False, e.body

    def file_move(self, source_file_path: str, dest_dir_path: str, new_name: str,
                  overwrite: bool = False) -> tuple[bool, str]:
        """文件移动

        Args:
            source_file_path (str): 源文件路径
            dest_dir_path (str): 目标目录
            new_name (str): 新文件名
            overwrite (bool): 是否覆盖(默认为False)

        Returns:
            tuple[bool, str] : (是否成功, 操作信息)
        """
        with xpan.ApiClient() as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            try:
                res = api.filemanagermove(
                    self.access_token, 1, json.dumps([{"path": source_file_path, "dest": dest_dir_path,
                                                       "newname": new_name, "ondup":
                                                           "overwrite" if overwrite else "fail"}]))
                if res["errno"] != 0:
                    return False, fxerr[res["info"][0]["errno"]]
                return True, fxerr[res["errno"]]
            except ApiException as e:
                return False, e.body

    def file_copy(self, source_file_path: str, dest_dir_path: str, new_name: str, overwrite: bool = False):
        """文件复制

        Args:
            source_file_path (str): 源文件路径
            dest_dir_path (str): 目标目录
            new_name (str): 新文件名
            overwrite (bool): 是否覆盖(默认为False)

        Returns:
            tuple[bool, str] : (是否成功, 操作信息)
        """
        with xpan.ApiClient() as api_client:
            api = filemanager_api.FilemanagerApi(api_client)
            try:
                res = api.filemanagercopy(
                    self.access_token, 1, json.dumps([{"path": source_file_path, "dest": dest_dir_path,
                                                       "newname": new_name, "ondup":
                                                           "overwrite" if overwrite else "fail"}]))
                if res["errno"] != 0:
                    return False, fxerr[res["info"][0]["errno"]]
                return True, fxerr[res["errno"]]
            except ApiException as e:
                return False, e.body
