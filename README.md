# FanBoxPosts_ScreenShot_Tools  
## FanBox投稿截图Python程序
**你可以通过它获取你关注的创作者的投稿的所有截图**  
*A Python program that can help you to get the screenshot of creator's posts.*
<br/>
<br/>
<br/>
## How to use?(如何使用？)  
**安装Python**  
>`建议Python版本>=3.8`
 
**安装Python软件包**  
1. >`pip install playwright`
2. >`pip install loguru`
3. >`pip install httpx`

**在__main__.py中运行程序**  
```
if __name__ == "__main__":
    # 输入'creator_id'运行后, 可在/images找到截图
    asyncio.get_event_loop().run_until_complete(
        get_shots(creator_id="<填fanbox上的创作者ID>")
    )
```
