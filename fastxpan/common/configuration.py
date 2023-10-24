class FxConfiguration:
    """Fast-Xpan配置类

    Args:
            client_id (str, optional): AppKey.
            device_id (str, optional): AppID.
            client_secret (str, optional): SecretKey.
            access_token (str, optional): Access Token.
    """

    def __init__(self, client_id: str = ..., device_id: str = ..., client_secret: str = ..., access_token: str = ...):
        self.client_id = client_id
        """AppKey"""
        self.device_id = device_id
        """AppID"""
        self.client_secret = client_secret
        """SecretKey"""
        self.access_token = access_token
        """Access Token"""
