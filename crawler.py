import logging
from abc import ABC, abstractmethod
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from models import RawCrawledProduct, RawCrawledProductImage, SupplierName

from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)


class CatalogCrawler(ABC):
    SUPPLIER: SupplierName

    def __init__(self) -> None:
        pass

    async def _fetch(
        self,
        url: str,
        *,
        method: str = "GET",
        data: dict | None = None,
        json: dict | None = None,
        headers: dict | None = None,
        retries: int = 3,
        backoff_base: float = 0.6,
        backoff_cap: float = 6.0,
        retry_on: tuple[int, ...] = (429, 500, 502, 503, 504),
    ) -> str | None:
        """Returns a non parsed HTML or XML document in string format."""
        pass

    @abstractmethod
    async def get_product_from_url(self, url: str) -> RawCrawledProduct | None:
        pass


class SkinCeuticalsCrawler(CatalogCrawler):
    def __init__(self) -> None:
        self.base_url = "https://www.skinceuticals.com/"

    async def _fetch(self, url: str) -> str:
        browsers = ["firefox", "webkit"]
        async with async_playwright() as p:
            for browser_type in browsers:
                browser = await p[browser_type].launch()
                page = await browser.new_page()
                await page.goto(url)

                html = await page.content()

                if "Just a moment" in html:
                    continue
                await browser.close()
                return html

            await browser.close()
            return None

    def _get_product_urls(self, soup):
        products = []

        for tile in soup.find_all("div", class_="c-product-tile__caption-inner"):
            title = tile.select_one(".c-product-tile__name")
            url = title.select_one("a")["href"]
            if url is not None:
                url = urljoin(self.base_url, url)
                products.append(url)
            else:
                print("No url found for", title, url)

        return products

    def _get_product_categories(self, soup, product_name):
        category = soup.find("div", class_="l-pdp__top-inner").text
        cleaned_category = category.split("  ")
        start_indexing = False
        product_categories = []
        for category in cleaned_category:
            if not start_indexing and category.lower() == "skincare":
                start_indexing = True
                continue
            elif start_indexing and category.lower() == product_name.lower():
                break
            if start_indexing and category:
                product_categories.append(category)
        return product_categories

    def _clean_text(self, text):
        return text.strip().replace("\n", "").replace("\t", "").replace("\r", "")

    def _collect_product_details_from_soup(self, soup, product_url):
        product_name = soup.find("h1", class_="c-product-main__name").text
        product_name = self._clean_text(product_name)
        price_spans = soup.find_all("span", class_="c-product-price__value")
        price = None
        for price_span in price_spans:
            if "$" in price_span.text:
                price = price_span.text
                price = price.replace("$", "")
                price = float(price)
                break
        product_categories = self._get_product_categories(soup, product_name)

        short_description = soup.find(
            "p", class_="c-product-main__short-description"
        ).text
        full_description = soup.find("div", "c-content-tile__description").text
        image_alternatives = soup.find(
            "div", class_="c-product-detail-image__alternatives"
        )
        images = []
        for image in image_alternatives.find_all("img"):
            images.append(RawCrawledProductImage(data=image["src"], alt=image["alt"]))

        if uom := soup.find("span", class_="c-variations-carousel__value"):
            uom = uom.text

        return RawCrawledProduct(
            supplier_sku="",
            manufacturer_sku="",
            name=product_name,
            url=product_url,
            gtin="",
            unspsc="",
            manufacturer_name="",
            current_price=price,
            category=product_categories,
            short_description=self._clean_text(short_description.split("...")[0]),
            description=self._clean_text(full_description),
            meta_description="",
            purchase_requirements="",
            images=images,
            attributes="",
            uom=[uom] if uom else [],
            documents=[],
        )

    async def get_product_from_url(self, url: str) -> RawCrawledProduct | None:
        html = await self._fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        return self._collect_product_details_from_soup(soup, url)

    async def run(self) -> List[RawCrawledProduct]:
        products_url = urljoin(self.base_url, "skincare")
        html = await self._fetch(products_url)
        soup = BeautifulSoup(html, "html.parser")
        product_urls = self._get_product_urls(soup)
        products = []
        for product_url in product_urls:
            product = await self.get_product_from_url(product_url)
            if product:
                products.append(product)
            return products
        return products
