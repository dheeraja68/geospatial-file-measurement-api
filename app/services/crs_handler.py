import geopandas as gpd


def get_measurement_crs(gdf):
    if gdf.crs is None:
        raise ValueError("Input file does not have a CRS")

    # If CRS is already projected and uses meters,
    # no transformation is required.
    if gdf.crs.is_projected:
        axis_units = gdf.crs.axis_info[0].unit_name

        if axis_units == "metre":
            return gdf

    # For geographic CRS or projected CRS using non-metric units,
    # transform to a suitable UTM CRS.
    projected_crs = gdf.estimate_utm_crs()

    if projected_crs is None:
        raise ValueError("Could not determine a suitable projected CRS")

    return gdf.to_crs(projected_crs)