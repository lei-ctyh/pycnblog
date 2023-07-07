import logging
import os
import tempfile


class Logger:
    def __init__(self, log_file='cnblogmd.log', log_level=logging.DEBUG):
        # 创建日志器
        self.logger = logging.getLogger()
        self.logger.setLevel(log_level)

        # 创建文件处理器并设置日志级别和格式
        log_full_path = os.path.join(tempfile.gettempdir(), log_file)
        file_handler = logging.FileHandler(filename=log_full_path,  encoding='utf-8')
        file_handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # 添加文件处理器到日志器
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


log = Logger()
