import logging as lg


class Log:
    @staticmethod
    def _config() -> lg.Logger:
        lg.basicConfig(level=lg.DEBUG)
        return lg.getLogger()

    @staticmethod
    def info(*msg) -> None:
        Log._config().info(msg)

    @staticmethod
    def debug(*msg) -> None:
        Log._config().debug(msg)

    @staticmethod
    def error(*msg) -> None:
        Log._config().error(msg)
