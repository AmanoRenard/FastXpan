fxerr = {
    -31066: "文件不存在",
    -10: "云端容量已满",
    -9: "文件或目录不存在",
    -8: "文件或目录已存在",
    -7: "文件或目录名错误或无权访问",
    -6: "身份验证失败",  # 1.access_token 是否有效; 2.授权是否成功；3.参考接入授权FAQ；4.阅读文档《使用入门->接入授权》章节。
    -3: "文件不存在",
    -1: "权益已过期",
    0: "请求成功",
    2: "参数错误",  # 1.检查必选参数是否都已填写；2.检查参数位置，有的参数是在url里，有的是在body里；3.检查每个参数的值是否正确。
    3: "不支持的开放API",
    6: "不允许接入用户数据",  # 建议10分钟之后用户再进行授权重试。
    10: "创建文件失败",
    11: "自己发送的分享",
    12: "批量转存出错",
    111: "Access Token 失效 / 有其他异步任务正在执行",
    255: "转存数量太多",
    2131: "该分享不存在",
    31023: "参数错误",
    31024: "没有申请上传权限",
    31034: "命中接口频控",
    31045: "access_token验证未通过，请检查access_token是否过期，用户授权时是否勾选网盘权限等。",
    31061: "文件已存在",
    31064: "没有上传文件到该目录的权限",  # path 上传文件的绝对路径格式：/apps/申请接入时填写的产品名称请参考《能力说明->限制条件->目录限制》
    31190: "文件不存在",
    31299: "第一个分片的大小小于4MB",
    31326: "命中防盗链，需检查User-Agent请求头是否正常。",
    31362: "签名错误，请检查链接地址是否完整。",
    31363: "分片缺失",
    31364: "超出分片大小限制",
    31365: "文件总大小超限",  # 授权用户为普通用户时，单个分片大小固定为4MB，单文件总大小上限为4GB
    42214: "文件基础信息查询失败",
    42905: "查询用户名失败，可重试"
}
