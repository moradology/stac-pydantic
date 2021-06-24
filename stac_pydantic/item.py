from datetime import datetime as dt
from functools import lru_cache
from typing import Dict, List, Optional, Tuple, Type, Union

from geojson_pydantic.features import Feature, FeatureCollection
from pydantic import constr, Field, validator, AnyUrl
from pydantic.datetime_parse import parse_datetime
import requests
import jsonschema

from stac_pydantic.api.extensions.context import ContextExtension
from stac_pydantic.extensions import Extensions
from stac_pydantic.links import Links
from stac_pydantic.shared import DATETIME_RFC339, Asset, BBox, StacCommonMetadata
from stac_pydantic.utils import decompose_model
from stac_pydantic.version import STAC_VERSION


class ItemProperties(StacCommonMetadata):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/item-spec/item-spec.md#properties-object
    """

    datetime: Union[dt, str] = Field(..., alias="datetime")

    @validator("datetime")
    def validate_datetime(cls, v, values):
        if v == "null":
            if not values["start_datetime"] and not values["end_datetime"]:
                raise ValueError(
                    "start_datetime and end_datetime must be specified when datetime is null"
                )

        if isinstance(v, str):
            return parse_datetime(v)

        return v

    class Config:
        extra = "allow"
        json_encoders = {dt: lambda v: v.strftime(DATETIME_RFC339)}


class Item(Feature):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/item-spec/item-spec.md
    """

    id: constr(min_length=1)
    stac_version: constr(min_length=1) = Field(STAC_VERSION, const=True)
    properties: ItemProperties
    assets: Dict[str, Asset]
    links: Links
    bbox: BBox
    stac_extensions: Optional[List[AnyUrl]]
    collection: Optional[str]

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


class ItemCollection(FeatureCollection):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0/item-spec/itemcollection-spec.md
    """

    stac_version: constr(min_length=1) = Field(STAC_VERSION, const=True)
    features: List[Item]
    stac_extensions: Optional[List[str]]
    links: Links
    context: Optional[ContextExtension]

    def to_dict(self, **kwargs):
        return self.dict(by_alias=True, exclude_unset=True, **kwargs)

    def to_json(self, **kwargs):
        return self.json(by_alias=True, exclude_unset=True, **kwargs)


def validate_item(item: Dict, reraise_exception: bool = False, **kwargs) -> bool:
    """
    Wrapper around ``item_model_factory`` for stac item validation
    """
    try:
        Item.parse_obj(item)
        if item["stac_extensions"]:
            for ext in item["stac_extensions"]:
                req = requests.get(ext)
                schema = req.json()
                jsonschema.validate(instance=item, schema=schema)
    except Exception:
        if reraise_exception:
            raise
        return False
    return True
