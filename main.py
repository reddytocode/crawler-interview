import asyncio

from crawler import SkinCeuticalsCrawler


async def main():
    crawler = SkinCeuticalsCrawler()
    product_details = await crawler.run()
    for product in product_details:
        print(product.model_dump_json())


asyncio.run(main())
