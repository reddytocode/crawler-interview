import asyncio
import logging

from crawler import SkinCeuticalsCrawler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    crawler = SkinCeuticalsCrawler()
    product_details = await crawler.run()
    for product in product_details:
        print(product.model_dump_json())


asyncio.run(main())
