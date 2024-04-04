import asyncio
import re

import httpx
import playwright.async_api
from playwright.async_api import async_playwright
from loguru import logger

from db import DefaultPath, create_first_dir
from utils import get_pages, get_post_urls


async def get_shots(creator_id: str):
    """获取截图"""
    async def get_shot(
            _url: str, _context: playwright.async_api.BrowserContext
    ) -> None:
        # 前往网址
        page = await context.new_page()
        await page.set_viewport_size(dict(width=width, height=height))
        await page.goto(url, timeout=114514, wait_until="load")
        logger.info(f"[FanBox]正在前往: {url}")

        # 等待投稿列表加载完毕
        logger.info(f"[FanBox]等待元素加载...")
        await page.wait_for_selector(
            'a[class^="CardPostItem"], [href^="/posts/"]',
            state="visible"
        )
        logger.info(f"[FanBox]元素加载完毕, 正在定位中...")

        # 获取投稿列表项
        post_items = await page.locator('a[class^="CardPostItem"]').all()
        logger.debug(f"[FanBox]定位完成, 待截图投稿: {[await i.get_attribute('href') for i in post_items]}")

        # 开始截图
        for item in post_items:
            logger.debug(f"[FanBox]正在截图-{(href := await item.get_attribute('href'))}")

            # 定位截图区域
            image = await page.wait_for_selector(f'a[href="{href}"]')
            box = await image.bounding_box()
            await page.mouse.wheel(delta_x=0, delta_y=box["y"] / 2)  # 使用滚轮

            # 等待渲染
            await asyncio.sleep(0.15)

            # 截图
            shot = await item.screenshot()
            logger.info(f"[FanBox]已截图-{href}")

            # 保存数据
            result = re.findall("/posts/(.\d+)", href)[0]
            save_path = DefaultPath / creator_id / f"{result}.jpg"
            with save_path.open(mode="wb") as f:
                f.write(shot)
            logger.info(f"[FanBox]已将截图保存至: {save_path}")
        return None

    # 初始化目录
    create_first_dir(DefaultPath)

    # 创建驱动
    logger.debug("[FanBox]正在创建上下文管理实例...")
    manager = await async_playwright().start()
    logger.debug("[FanBox]创建完毕!")
    logger.info("[FanBox]正在创建'Chromium'驱动(无头模式)...")
    browser = await manager.chromium.launch(headless=False)
    logger.info("[FanBox]驱动创建完毕!")

    # 获取待截图页面URL
    async with httpx.AsyncClient() as client:
        pages = await get_pages(client, creator_id)
    urls = get_post_urls(creator_id, pages)

    # 设置页面环境
    context = await browser.new_context(locale="zh-CN")
    width, height = 2560, 1440
    logger.debug(f"[FanBox]设定页面环境, 设定页面尺寸为{width}x{height}, 正在创建实例...")

    # 初始化图片保存路径
    create_first_dir(DefaultPath/creator_id)

    # 开始准备截图
    for url in urls:
        await asyncio.create_task(get_shot(url, context))
        logger.success(f"{'-'*50}[FanBox]完成当前页面的截图任务{'-'*50}")
    logger.success("[FanBox]所有截图任务均已完成!")


if __name__ == "__main__":
    # 输入'creator_id'运行后, 可在/images找到截图
    asyncio.get_event_loop().run_until_complete(
        get_shots(creator_id="mklntic")
    )
