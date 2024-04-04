import os
from pathlib import Path

from loguru import logger


DefaultPath = Path(__file__).parent/"images"


def create_first_dir(dir_path: Path):
    """
    创建文件目录
    :param dir_path: 文件目录
    :return: True-创建目录成功 None-目录已存在
    """
    if not os.path.exists(dir_path):
        logger.warning(f"[FanBox]目录缺失,创建路径于{dir_path}")
        os.mkdir(dir_path)


__all__ = ["DefaultPath", "create_first_dir"]
