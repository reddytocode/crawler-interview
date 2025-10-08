import asyncio
import logging

from crawler import SkinCeuticalsCrawler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    crawler = SkinCeuticalsCrawler()
    await crawler.run()


asyncio.run(main())
