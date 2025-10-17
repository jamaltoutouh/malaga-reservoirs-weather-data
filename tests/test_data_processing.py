"""
Unit tests for data processing utilities.
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_processing.loader import ReservoirDataLoader
from data_processing.cleaner import ReservoirDataCleaner
from data_processing.validator import DataValidator


class TestReservoirDataLoader(unittest.TestCase):
    """Test cases for ReservoirDataLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create sample test data
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=10),
            'embalse_codigo': ['S19'] * 10,
            'embalse_nombre': ['CASASOLA'] * 10,
            'embalse_provincia': ['MALAGA'] * 10,
            'embalse_reserva': np.random.uniform(10, 20, 10),
            'embalse_porcentaje': np.random.uniform(40, 80, 10),
            'meteo_temp_max': np.random.uniform(15, 25, 10),
            'meteo_temp_min': np.random.uniform(5, 15, 10),
            'meteo_precipitacion': np.random.uniform(0, 10, 10)
        })
    
    def test_get_available_reservoirs(self):
        """Test getting available reservoirs."""
        loader = ReservoirDataLoader("data/reservoir-weather")
        reservoirs = loader._get_available_reservoirs()
        self.assertIsInstance(reservoirs, list)
        self.assertIn('CASASOLA', reservoirs)
        self.assertNotIn('test', reservoirs)  # Should exclude test files


class TestReservoirDataCleaner(unittest.TestCase):
    """Test cases for ReservoirDataCleaner class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5),
            'embalse_porcentaje': [45.0, 50.123456789, 55.0, np.nan, 60.0],
            'meteo_temp_max': [25.123456789, 30.0, 28.0, 26.0, 29.0],
            'meteo_temp_min': [15.0, 20.0, 18.0, 16.0, np.nan],
            'meteo_precipitacion': [0.0, 5.5, 0.0, 2.3, 0.0]
        })
    
    def test_clean_numeric_columns(self):
        """Test numeric column cleaning."""
        cleaned = ReservoirDataCleaner.clean_numeric_columns(self.sample_data)
        
        # Check that floating point precision is fixed
        self.assertEqual(cleaned['embalse_porcentaje'].iloc[1], 50.1)
        self.assertEqual(cleaned['meteo_temp_max'].iloc[0], 25.12)
    
    def test_handle_missing_values(self):
        """Test missing value handling."""
        filled = ReservoirDataCleaner.handle_missing_values(
            self.sample_data, strategy='forward_fill'
        )
        
        # Check that missing values are filled
        self.assertFalse(filled['embalse_porcentaje'].isna().any())
        self.assertFalse(filled['meteo_temp_min'].isna().any())
    
    def test_add_derived_features(self):
        """Test derived feature creation."""
        enhanced = ReservoirDataCleaner.add_derived_features(self.sample_data)
        
        # Check that new features are added
        self.assertIn('year', enhanced.columns)
        self.assertIn('month', enhanced.columns)
        self.assertIn('season', enhanced.columns)
        self.assertIn('meteo_temp_range', enhanced.columns)


class TestDataValidator(unittest.TestCase):
    """Test cases for DataValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=5),
            'embalse_porcentaje': [45.0, 50.0, 55.0, 120.0, 60.0],  # One outlier
            'meteo_temp_max': [25.0, 30.0, 28.0, 26.0, 29.0],
            'meteo_temp_min': [35.0, 20.0, 18.0, 16.0, 19.0],  # First value inconsistent
            'meteo_temp_media': [20.0, 25.0, 23.0, 21.0, 24.0]
        })
    
    def test_check_data_completeness(self):
        """Test data completeness checking."""
        completeness = DataValidator.check_data_completeness(self.sample_data)
        
        self.assertIsInstance(completeness, dict)
        self.assertEqual(completeness['date'], 100.0)
        self.assertEqual(completeness['embalse_porcentaje'], 100.0)
    
    def test_validate_weather_consistency(self):
        """Test weather data consistency validation."""
        inconsistencies = DataValidator.validate_weather_consistency(self.sample_data)
        
        # Should detect temperature inconsistency (min > max in first row)
        self.assertIn('temperature_order', inconsistencies)
        self.assertIn(0, inconsistencies['temperature_order'])
    
    def test_check_reservoir_consistency(self):
        """Test reservoir data consistency."""
        inconsistencies = DataValidator.check_reservoir_consistency(self.sample_data)
        
        # Should detect percentage out of bounds (120%)
        self.assertIn('percentage_out_of_bounds', inconsistencies)
        self.assertIn(3, inconsistencies['percentage_out_of_bounds'])


if __name__ == '__main__':
    unittest.main()
