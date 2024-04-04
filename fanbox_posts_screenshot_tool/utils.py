from typing import List

import httpx
from loguru import logger


async def get_pages(
        client: httpx.AsyncClient, creator_id: str
) -> int:
    """
    获取投稿总页数
    :param client: httpx.AsyncClient
    :param creator_id: 创作者ID
    :return: 页数
    """
    res = await client.get(
        url=f"https://api.fanbox.cc/post.paginateCreator?creatorId={creator_id}",
        headers={
            "Origin": (url := f"https://{creator_id}.fanbox.cc"),
            "Referer": url
        }
    )
    res.raise_for_status()
    logger.debug(f"访问API, 获得数据: {(data := res.json()['body'])}")
    assert (pages := len(data)) > 0, f"用户(ID: {creator_id})没有投稿!"
    logger.info(f"总截图页面数-{pages}")
    return pages


def get_post_urls(creator_id: str, pages: int) -> List[str]:
    """
    获取投稿网址
    :param creator_id: 创作者ID
    :param pages: 页数
    :return: List[str]
    """
    assert pages > 0, f"用户(ID: {creator_id})没有投稿!"
    return [f"https://{creator_id}.fanbox.cc/posts?page={p}" for p in range(1, pages+1)]


__all__ = ["get_pages", "get_post_urls"]
