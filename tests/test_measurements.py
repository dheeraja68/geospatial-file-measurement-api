from shapely.geometry import Polygon, LineString, Point

from app.services.measurement import calculate_measurement


def test_polygon_area():
    polygon = Polygon([
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10)
    ])

    result = calculate_measurement(polygon)

    assert result["geometry_type"] == "Polygon"
    assert result["area_sq_m"] == 100
    assert result["length_m"] is None


def test_linestring_length():
    line = LineString([
        (0, 0),
        (3, 4)
    ])

    result = calculate_measurement(line)

    assert result["geometry_type"] == "LineString"
    assert result["length_m"] == 5
    assert result["area_sq_m"] is None


def test_point():
    point = Point(10, 20)

    result = calculate_measurement(point)

    assert result["geometry_type"] == "Point"
    assert result["area_sq_m"] is None
    assert result["length_m"] is None