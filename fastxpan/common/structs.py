from datetime import datetime


class FxFile(dict):
    """FastXpan文件信息类型

    Attributes:
        fs_id: 文件在云端的ID(int)
        name: 文件名称(str)
        isdir: 是否为目录(int)
        path: 文件的绝对路径(str)
        size: 文件大小(int)
        size_str: 格式化文件大小(str)
        modified_date: 修改日期(str)
    """

    def __init__(self, data: dict):
        super().__init__()
        self["fs_id"] = data["fs_id"]
        self["isdir"] = data["isdir"]
        self["modified_date"] = f"{datetime.fromtimestamp(data['server_mtime'])}"
        self["name"] = data["name"]
        self["path"] = data["path"]
        self["size"] = data["size"]
        self["size_str"] = f"{data['size'] / 1024:.2f}KB" if \
            data['size'] < 1048576 else f"{data['size'] / 1048576:.2f}MB"
        self.fs_id = self["fs_id"]
        """文件在云端的ID(int)"""
        self.isdir = self["isdir"]
        """是否为目录(int)"""
        self.modified_date = self["modified_date"]
        """修改日期(str)"""
        self.name = self["server_filename"]
        """文件名称(str)"""
        self.path = self["path"]
        """文件的绝对路径(str)"""
        self.size = self["size"]
        """文件大小(int)"""
        self.size_str = self["size_str"]
        """格式化文件大小(str)"""


class FxFileMeta(dict):
    """FastXpan文件详细信息类型

    Attributes:
        category: 文件类型，1 视频、2 音频、3 图片、4 文档、5 应用、6 其他、7 种子(int)
        fs_id: 文件在云端的ID(int)
        isdir: 是否为目录，0 文件、1 目录(int)
        local_ctime: 文件在客户端修改时间(int)
        local_mtime: 文件在客户端创建时间(int)
        md5: 云端哈希（非文件真实MD5），非文件类型为0(int)
        path: 文件的绝对路径(str)
        server_ctime: 文件在服务器创建时间(int)
        server_filename: 文件名称(str)
        server_mtime: 文件在服务器修改时间(int)
        size: 文件大小(int)
        size_str: 格式化文件大小(str)
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
        self["size_str"] = f"{data['size'] / 1024:.2f}KB" if \
            data['size'] < 1048576 else f"{data['size'] / 1048576:.2f}MB"
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
        """云端哈希（非文件真实MD5），非文件类型为0"(int)"""
        self.path = data["path"]
        """文件的绝对路径(str)"""
        self.server_ctime = data["server_ctime"]
        """文件在服务器创建时间(int)"""
        self.server_filename = data["server_filename"]
        """文件名称(str)"""
        self.server_mtime = data["server_mtime"]
        """文件在服务器修改时间(int)"""
        self.size = data["size"]
        """文件大小(int)"""
        self.size_str = self["size_str"]
        """格式化文件大小(str)"""


class FxImage(dict):
    """FastXpan图片信息类型

    Attributes:
        fs_id: 文件ID(int)
        modified_date: 修改日期(str)
        path: 图片路径(str)
        size: 图片大小(int)
        size_str: 格式化图片大小(str)
        thumbs: 四种图片略缩图URL(dict)
    """

    def __init__(self, data: dict):
        super().__init__()
        self["fs_id"] = data["fs_id"]
        self["modified_date"] = f"{datetime.fromtimestamp(data['server_mtime'])}"
        self["size_str"] = f"{data['size'] / 1024:.2f}KB" if \
            data['size'] < 1048576 else f"{data['size'] / 1048576:.2f}MB"
        self["size"] = data["size"]
        self["thumbs"] = data["thumbs"]
        self["path"] = data["path"]
        self.fs_id = self["fs_id"]
        """文件ID"""
        self.modified_date = self["modified_date"]
        """修改日期"""
        self.size_str = self["size_str"]
        """格式化图片大小"""
        self.size = self["size"]
        """图片大小"""

        class _Thumbs(dict):
            """四种图片略缩图URL

            Attributes:
                icon: 图片图标URL
                url1: 小尺寸略缩图URL
                url2: 中尺寸略缩图URL
                url3: 大尺寸略缩图URL
            """

            def __init__(self, _thumbs: dict):
                super().__init__()
                self["icon"] = _thumbs["icon"]
                self["url1"] = _thumbs["url1"]
                self["url2"] = _thumbs["url2"]
                self["url3"] = _thumbs["url3"]
                self.icon = self["icon"]
                self.url1 = self["url1"]
                self.url2 = self["url2"]
                self.url3 = self["url3"]

        self.thumbs = _Thumbs(self["thumbs"])
        """四种图片略缩图URL"""
        self.path = data["path"]
        """图片路径"""


class FxUser(dict):
    """FastXpan用户信息类型

    Attributes:
        baidu_name: 百度用户名(str)
        netdisk_name: 网盘用户名(str)
        avatar_url: 头像URL(str)
        vip_type: 会员类型，0普通用户、1普通会员、2超级会员(int)
        user_id: 百度用户ID(int)
    """
    def __init__(self, data: dict):
        super().__init__()
        self["baidu_name"] = data["baidu_name"]
        self["avatar_url"] = data["avatar_url"]
        self["vip_type"] = data["vip_type"]
        self["user_id"] = data["uk"]
        self.baidu_name = self["baidu_name"]
        """百度用户名(str)"""
        self.avatar_url = self["avatar_url"]
        """头像URL(str)"""
        self.vip_type = self["vip_type"]
        """会员类型，0普通用户、1普通会员、2超级会员(int)"""
        self.user_id = self["user_id"]
        """百度用户ID(int)"""


class FxUserQuota(dict):
    def __init__(self, data: dict):
        super().__init__()
        self["total"] = data["total"]
        self["used"] = data["used"]
        self.total = self["total"]
        """总容量(int)"""
        self.used = self["used"]
        """已使用容量(int)"""

