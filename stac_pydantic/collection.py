from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from stac_pydantic.catalog import Catalog
from stac_pydantic.shared import Asset, NumType, Provider


class SpatialExtent(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0-beta.1/collection-spec/collection-spec.md#spatial-extent-object
    """

    bbox: List[List[NumType]]


class TimeInterval(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0-beta.1/collection-spec/collection-spec.md#temporal-extent-object
    """

    interval: List[List[Union[str, None]]]


class Extent(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0-beta.1/collection-spec/collection-spec.md#extent-object
    """

    spatial: SpatialExtent
    temporal: TimeInterval


class Range(BaseModel):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0-beta.1/collection-spec/collection-spec.md#stats-object
    """

    minimum: Union[NumType, str]
    maximum: Union[NumType, str]


class Collection(Catalog):
    """
    https://github.com/radiantearth/stac-spec/blob/v1.0.0-beta.1/collection-spec/collection-spec.md
    """

    assets: Dict[str, Asset]
    license: str
    extent: Extent
    title: Optional[str]
    keywords: Optional[List[str]]
    providers: Optional[List[Provider]]
    summaries: Optional[Dict[str, Union[Range, List[Any], Dict[str, Any]]]]
    type: str = "collection"
