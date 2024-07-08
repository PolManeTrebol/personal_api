class SingletonMeta(type):
    """
    Singleton metaclass
    """
    _instances: dict = {}

    def __call__(cls, *args, **kwargs) -> None:  # type: ignore
        if cls not in cls._instances:
            instance: SingletonMeta = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
