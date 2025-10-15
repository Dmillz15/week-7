"""
Script to load geographical data into a pandas DataFrame and save it as a CSV file.
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import pandas as pd
import numpy as np


def get_geolocator(agent='h501-student'):
    """
    Initiate a Nominatim geolocator instance given an `agent`.
    """
    return Nominatim(user_agent=agent)


def fetch_location_data(geolocator, loc):
    """
    Fetch latitude, longitude, and type for a given location string.

    Returns a dictionary with Location, Latitude, Longitude, and Type.
    """
    try:
        location = geolocator.geocode(loc, timeout=10)

        if location is None:
            return {
                "Location": loc,
                "Latitude": np.nan,
                "Longitude": np.nan,
                "Type": np.nan
            }

        loc_type = location.raw.get("type", np.nan)

        return {
            "Location": loc,
            "Latitude": location.latitude,
            "Longitude": location.longitude,
            "Type": loc_type
        }

    except (GeocoderServiceError, Exception) as e:
        print(f"Error fetching location '{loc}': {e}")
        return {
            "Location": loc,
            "Latitude": np.nan,
            "Longitude": np.nan,
            "Type": np.nan
        }


def build_geo_dataframe(locations, agent='h501-student'):
    """
    Build a pandas DataFrame containing geographic info for given locations.
    """
    geolocator = get_geolocator(agent)
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]
    return pd.DataFrame(geo_data, columns=["Location", "Latitude", "Longitude", "Type"])


if __name__ == "__main__":
    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa"
    ]

    df = build_geo_dataframe(locations)

    try:
        df.to_csv("./geo_data.csv", index=False)
        print("geo_data.csv saved successfully.")
    except Exception as e:
        print(f"Error saving CSV: {e}")
