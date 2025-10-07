import pytest
from crawler import SkinCeuticalsCrawler


def test_get_product_urls():
    crawler = SkinCeuticalsCrawler()
    soup = None
    res = crawler._get_product_urls(soup)
    assert res == []

def test_collect_product_details_from_soup():
    crawler = SkinCeuticalsCrawler()
    assert True
