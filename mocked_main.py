"""
I had a problem with cloudfare to emulate the clicks on the "Load More Products" button.
So, I manually clicked on the Load More button, and then saved the html.
This file uses that html to run the crawler.
It mocks the "all products" page. But it still goes into each product page to get the details.
"""

import asyncio
import logging

from crawler import SkinCeuticalsCrawler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    crawler = SkinCeuticalsCrawler()
    await crawler.run_list_of_all_products_mocked()


asyncio.run(main())
