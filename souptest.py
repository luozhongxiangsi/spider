from bs4 import BeautifulSoup
import asyncio
from pyppeteer import launch
import pandas as pd

headers = {
            "Accept": "text/html,application/xhtml+xml,"
                      "application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "Keep-Alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/55.0.2883.87 Safari/537.36",
        }


async def get(sem, url_):
    # headless参数设为False，则变成有头模式
    async with sem:
        browser = await launch(
        # headless=False
        )
        page = await browser.newPage()
        # 设置页面视图大小
        await page.setViewport(viewport={'width': 1280, 'height': 800})
        # 是否启用JS，enabled设为False，则无渲染效果
        await page.setJavaScriptEnabled(enabled=True)
        await page.goto(url_)
        try:
            soup = BeautifulSoup(await page.content(), 'lxml')
        # print(soup.tbody)
            print(type(soup))
            infos = soup.tbody.find_all('td')

            infos = [infos[i:i+7] for i in range(0, len(infos)+1, 7)]
        # print(infos)
            for x in infos:
                try:
                    print((x[0].contents[0], x[1].contents[0], x[2].contents[0], x[3].contents[0], x[4].contents[0], x[5].contents[0], x[6].contents[0]))
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
    # 关闭浏览器
        await browser.close()


if __name__ == '__main__':
    tasks = []
    for x in range(1, 20):
        url = f'https://www.kuaidaili.com/free/inha/{x}/'
        # 设置并发的数量
        sem = asyncio.Semaphore(1)
        loop = asyncio.get_event_loop()
        task = loop.create_task(get(sem, url))
        tasks.append(task)
    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))






