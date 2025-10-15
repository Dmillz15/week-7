import unittest
import pandas as pd
import numpy as np
from loader import build_geo_dataframe


class TestLoader(unittest.TestCase):

    def test_valid_locations(self):
        """Test that known locations return correct coordinates and types."""

        locations = [
            "Museum of Modern Art",
            "USS Alabama Battleship Memorial Park"
        ]

        df = build_geo_dataframe(locations)

        # Expected values
        expected = pd.DataFrame({
            "Location": ["Museum of Modern Art", "USS Alabama Battleship Memorial Park"],
            "Latitude": [40.7618552, 30.684373],
            "Longitude": [-73.9782438, -88.015316],
            "Type": ["museum", "park"]
        })

        # Compare ignoring small rounding differences
        pd.testing.assert_frame_equal(
            df.reset_index(drop=True),
            expected,
            check_exact=False,
            check_dtype=False,
            atol=0.01  # small tolerance for rounding from geocoding
        )

    def test_invalid_location(self):
        """Test that a nonsense location returns NaN values for coordinates and type."""

        df = build_geo_dataframe(["asdfqwer1234"])

        # Should only have one row
        self.assertEqual(len(df), 1)
        self.assertEqual(df.loc[0, "Location"], "asdfqwer1234")
        self.assertTrue(pd.isna(df.loc[0, "Latitude"]))
        self.assertTrue(pd.isna(df.loc[0, "Longitude"]))
        self.assertTrue(pd.isna(df.loc[0, "Type"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
