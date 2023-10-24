from datetime import datetime


class FxFile(dict):
    """FastXpan文件信息类型

    Args:
        data: {
            "fs_id": 文件在云端的ID(int),
            "name": 文件名称(str),
            "isdir": 是否为目录(int),
            "path": 文件的绝对路径(str),
            "size": 文件大小，单位B(int),
            "modified_date": 修改日期(str)}
    """

    def __init__(self, data: dict = ...):
        super().__init__()
        self.fs_id = data["fs_id"]
        """文件在云端的ID(int)"""
        self.isdir = data["isdir"]
        """是否为目录(int)"""
        self.modified_date = f"{datetime.fromtimestamp(data['server_mtime'])}"
        """修改日期(str)"""
        self.name = data["server_filename"]
        """文件名称(str)"""
        self.path = data["path"]
        """文件的绝对路径(str)"""
        self.size = f"{data['size'] / 1024:.2f}KB" if data['size'] < 1048576 else f"{data['size'] / 1048576:.2f}MB"
        """文件大小，单位B(int)"""
        self["fs_id"] = self.fs_id
        self["isdir"] = self.isdir
        self["modified_date"] = self.modified_date
        self["name"] = self.name
        self["path"] = self.path
        self["size"] = self.size


class FxFile2(dict):
    """FastXpan文件信息类型

    Args:
        data: {
            "fs_id": 文件在云端的ID(int),
            "name": 文件名称(str),
            "isdir": 是否为目录(int),
            "path": 文件的绝对路径(str),
            "size": 文件大小，单位B(int),
            "modified_date": 修改日期(int)}
    """

    def __init__(self, data: dict):
        super().__init__()
        self["fs_id"] = data["fs_id"]
        self["isdir"] = data["isdir"]
        self["modified_date"] = f"{datetime.fromtimestamp(data['server_mtime'])}"
        self["name"] = data["server_filename"]
        self["path"] = data["path"]
        self["size"] = f"{data['size'] / 1024:.2f}KB" if data['size'] < 1048576 else f"{data['size'] / 1048576:.2f}MB"


class FxFileMeta(dict):
    """FastXpan文件详细信息类型

    Args:
        data: {
            "category": 文件类型，1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子(int),
            "fs_id": 文件在云端的ID(int),
            "isdir": 是否为目录，0 文件、1 目录(int),
            "local_ctime": 文件在客户端修改时间(int),
            "local_mtime": 文件在客户端创建时间(int),
            "md5": "云端哈希（非文件真实MD5），非文件类型为0"(int),
            "path": 文件的绝对路径(str),
            "server_ctime": 文件在服务器创建时间(int),
            "server_filename": 文件名称(str),
            "server_mtime": 文件在服务器修改时间(int),
            "size": 文件大小，单位B(int),
    """

    def __init__(self, data: dict = ...):
        super().__init__()
        self.category = data["category"]
        """文件类型，1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子(int)"""
        self.fs_id = data["fs_id"]
        """文件在云端的ID(int)"""
        self.isdir = data["isdir"]
        """是否为目录，0 文件、1 目录(int)"""
        self.local_ctime = data["local_ctime"]
        """文件在客户端修改时间(int)"""
        self.local_mtime = data["local_mtime"]
        """文件在客户端创建时间(int)"""
        self.md5 = data["md5"] if not data["isdir"] else 0
        self.path = data["path"]
        self.server_ctime = data["server_ctime"]
        self.server_filename = data["server_filename"]
        self.server_mtime = data["server_mtime"]
        self.size = data["size"]
        self["category"] = data["category"]
        self["fs_id"] = data["fs_id"]
        self["isdir"] = data["isdir"]
        self["local_ctime"] = data["local_ctime"]
        self["local_mtime"] = data["local_mtime"]
        self["md5"] = data["md5"] if not data["isdir"] else 0
        self["path"] = data["path"]
        self["server_ctime"] = data["server_ctime"]
        self["server_filename"] = data["server_filename"]
        self["server_mtime"] = data["server_mtime"]
        self["size"] = data["size"]


class FxFileMeta2(dict):
    """FastXpan文件详细信息类型

    Args:
        data: {
            "category": 文件类型，1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子(int),
            "fs_id": 文件在云端的ID(int),
            "isdir": 是否为目录，0 文件、1 目录(int),
            "local_ctime": 文件在客户端修改时间(int),
            "local_mtime": 文件在客户端创建时间(int),
            "md5": "云端哈希（非文件真实MD5），非文件类型为0"(int),
            "path": 文件的绝对路径(str),
            "server_ctime": 文件在服务器创建时间(int),
            "server_filename": 文件名称(str),
            "server_mtime": 文件在服务器修改时间(int),
            "size": 文件大小，单位B(int),
    """

    def __init__(self, data: dict):
        super().__init__()
        self["category"] = data["category"]
        self["fs_id"] = data["fs_id"]
        self["isdir"] = data["isdir"]
        self["local_ctime"] = data["local_ctime"]
        self["local_mtime"] = data["local_mtime"]
        self["md5"] = data["md5"] if not data["isdir"] else 0
        self["path"] = data["path"]
        self["server_ctime"] = data["server_ctime"]
        self["server_filename"] = data["server_filename"]
        self["server_mtime"] = data["server_mtime"]
        self["size"] = data["size"]


class FxImage(dict):
    """FastXpan图片信息类型

    Args:
        {"fs_id": 文件ID,
   "modified_date": 修改日期,
   "path": "图片路径",
   "size": "图片大小",
   "thumbs": {"icon": "图片图标",
              "url1": "小尺寸略缩图",
              "url2": "中尺寸略缩图",
              "url3": "大尺寸略缩图"}}

    """

    def __init__(self, data: dict):
        super().__init__()
        self["fs_id"] = data["fs_id"]
        self["modified_date"] = f"{datetime.fromtimestamp(data['server_mtime'])}"
        self["size"] = f"{data['size'] / 1024:.2f}KB" if data['size'] < 1048576 else f"{data['size'] / 1048576:.2f}MB"
        self["thumbs"] = data["thumbs"]
        self["path"] = data["path"]
