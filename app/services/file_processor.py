import geopandas as gpd

from app.services.crs_handler import get_measurement_crs
from app.services.measurement import calculate_measurement


def process_file(file_path, file_type):

    # Read the file
    if file_type == "kml":
        gdf = gpd.read_file(file_path, driver="KML")

    elif file_type == "zip":
      try:
        gdf = gpd.read_file(file_path)
      except Exception:
        raise ValueError(
            "Invalid ZIP file or ZIP does not contain a valid Shapefile."
        )
    else:
        raise ValueError("Unsupported file type")

    # Save original CRS
    original_crs = str(gdf.crs)

    # Convert to projected CRS
    gdf = get_measurement_crs(gdf)

    # Save measurement CRS
    measurement_crs = str(gdf.crs)

    features = []

    # Process every feature
    for index, row in gdf.iterrows():

        measurement = calculate_measurement(row.geometry)

        feature = {
            "feature_index": index,
            "geometry_type": measurement["geometry_type"],
            "geometry": row.geometry.wkt,
            "properties": {
                key: None if value != value else value
                for key, value in row.drop("geometry").to_dict().items()
          },
            "area_sq_m": measurement["area_sq_m"],
            "length_m": measurement["length_m"]
        }

        features.append(feature)

    return {
        "original_crs": original_crs,
        "measurement_crs": measurement_crs,
        "feature_count": len(features),
        "features": features
    }