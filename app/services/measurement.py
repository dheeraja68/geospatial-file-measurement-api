def calculate_measurement(geometry):

    geometry_type = geometry.geom_type

    if geometry_type == "Polygon":
        return {
            "geometry_type": geometry_type,
            "area_sq_m": geometry.area,
            "length_m": None
        }

    elif geometry_type == "LineString":
        return {
            "geometry_type": geometry_type,
            "area_sq_m": None,
            "length_m": geometry.length
        }

    elif geometry_type == "Point":
        return {
            "geometry_type": geometry_type,
            "area_sq_m": None,
            "length_m": None
        }

    else:
        return {
            "geometry_type": geometry_type,
            "area_sq_m": None,
            "length_m": None
        }