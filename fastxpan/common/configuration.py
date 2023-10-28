class FxConfiguration:
    """Fast-Xpan配置类

    Args:
        access_token (str, optional): Access Token.
        client_id (str, optional): AppKey.
        device_id (str, optional): AppID.
        client_secret (str, optional): SecretKey.
    """

    def __init__(self, access_token: str = ..., client_id: str = ..., device_id: str = ..., client_secret: str = ...):
        self.access_token = access_token
        """Access Token"""
        self.client_id = client_id
        """AppKey"""
        self.device_id = device_id
        """AppID"""
        self.client_secret = client_secret
        """SecretKey"""
