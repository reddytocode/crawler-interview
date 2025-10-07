from enum import StrEnum

from pydantic import BaseModel, Field


class SupplierName(StrEnum):
    DELASCO = "Delasco"
    MCKESSON = "McKesson"
    HENRY_SCHEIN = "Henry Schein"


class RawCrawledProductImage(BaseModel):
    data: str
    alt: str


class RawCrawledProduct(BaseModel):
    # Basic Information
    supplier_sku: str
    manufacturer_sku: str
    name: str
    url: str

    # Product Details
    gtin: str | None = None
    unspsc: str | None = None

    # Brand
    manufacturer_name: str | None = None

    # Pricing
    current_price: float | None = None

    # Categories
    category: list[str]

    # Descriptions
    short_description: str = ""
    description: str
    meta_description: str
    purchase_requirements: str | None = None

    # Images
    images: list[RawCrawledProductImage]

    attributes: str = "{}"
    uom: list[str] = Field(default_factory=list)

    documents: list[str] = Field(default_factory=list)
