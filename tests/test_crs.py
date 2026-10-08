import geopandas as gpd
from shapely.geometry import Point

from app.services.crs_handler import get_measurement_crs


def test_missing_crs():
    gdf = gpd.GeoDataFrame(
        {"name": ["test"]},
        geometry=[Point(78.4, 17.5)]
    )

    try:
        get_measurement_crs(gdf)
        assert False
    except ValueError as e:
        assert str(e) == "Input file does not have a CRS"


def test_geographic_crs_is_projected():
    gdf = gpd.GeoDataFrame(
        {"name": ["test"]},
        geometry=[Point(78.4, 17.5)],
        crs="EPSG:4326"
    )

    result = get_measurement_crs(gdf)

    assert result.crs.is_projected