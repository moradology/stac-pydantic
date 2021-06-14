from urllib.parse import urlparse

from .datacube import DatacubeExtension
from .eo import ElectroOpticalExtension
from .item_assets import ItemAssetExtension
from .label import LabelExtension
from .pc import PointCloudExtension
from .projection import ProjectionExtension
from .sar import SARExtension
from .sat import SatelliteExtension
from .sci import ScientificCitationExtension
from .timestamps import TimestampsExtension
from .version import VersionExtension
from .view import ViewExtension


class Extensions:
    datacube = DatacubeExtension
    eo = ElectroOpticalExtension
    item_assets = ItemAssetExtension
    label = LabelExtension
    pointcloud = PointCloudExtension
    projection = ProjectionExtension
    sar = SARExtension
    sat = SatelliteExtension
    scientific = ScientificCitationExtension
    timestamps = TimestampsExtension
    version = VersionExtension
    view = ViewExtension

    aliases = {}

    @classmethod
    def register(cls, k, v, alias=None):
        setattr(cls, k, v)

        if alias:
            cls.aliases[alias] = k

    @classmethod
    def get(cls, k):
        if not urlparse(k).scheme:
            k = k.replace("-", "_")
        try:
            return getattr(cls, k)
        except AttributeError:
            try:
                return getattr(cls, cls.aliases[k])
            except KeyError:
                raise AttributeError(f"Invalid extension name or alias: {k}")
