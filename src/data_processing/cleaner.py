"""
Data cleaning and preprocessing utilities.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional


class ReservoirDataCleaner:
    """
    Utility class for cleaning and preprocessing reservoir weather data.
    """
    
    @staticmethod
    def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean numeric columns by handling floating point precision issues.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with cleaned numeric columns
        """
        df_clean = df.copy()
        
        # Define numeric columns
        numeric_columns = [
            'embalse_reserva', 'embalse_porcentaje',
            'meteo_temp_max', 'meteo_temp_min', 'meteo_temp_media',
            'meteo_humedad_max', 'meteo_humedad_min', 'meteo_humedad_media',
            'meteo_vel_viento', 'meteo_vel_viento_max', 'meteo_dir_viento',
            'meteo_radiacion', 'meteo_precipitacion'
        ]
        
        # Round to reasonable precision to fix floating point issues
        for col in numeric_columns:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                if col in ['embalse_reserva']:
                    df_clean[col] = df_clean[col].round(3)
                elif col in ['embalse_porcentaje']:
                    df_clean[col] = df_clean[col].round(1)
                elif 'temp' in col:
                    df_clean[col] = df_clean[col].round(2)
                elif 'humedad' in col:
                    df_clean[col] = df_clean[col].round(1)
                elif 'viento' in col or 'dir_viento' in col:
                    df_clean[col] = df_clean[col].round(2)
                elif col in ['meteo_radiacion', 'meteo_precipitacion']:
                    df_clean[col] = df_clean[col].round(2)
        
        return df_clean
    
    @staticmethod
    def validate_ranges(df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate data ranges and flag outliers.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with validated ranges
        """
        df_validated = df.copy()
        
        # Define reasonable ranges for validation
        ranges = {
            'embalse_porcentaje': (0, 100),
            'meteo_temp_max': (-10, 50),
            'meteo_temp_min': (-15, 45),
            'meteo_temp_media': (-12, 47),
            'meteo_humedad_max': (0, 100),
            'meteo_humedad_min': (0, 100),
            'meteo_humedad_media': (0, 100),
            'meteo_vel_viento': (0, 50),
            'meteo_vel_viento_max': (0, 100),
            'meteo_dir_viento': (0, 360),
            'meteo_radiacion': (0, 40),
            'meteo_precipitacion': (0, 200)
        }
        
        # Flag values outside reasonable ranges
        for col, (min_val, max_val) in ranges.items():
            if col in df_validated.columns:
                mask = (df_validated[col] < min_val) | (df_validated[col] > max_val)
                if mask.any():
                    print(f"Warning: {mask.sum()} values in {col} outside range [{min_val}, {max_val}]")
        
        return df_validated
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, 
                            strategy: str = 'interpolate') -> pd.DataFrame:
        """
        Handle missing values in the dataset.
        
        Args:
            df: Input DataFrame
            strategy: Strategy for handling missing values ('interpolate', 'forward_fill', 'drop')
            
        Returns:
            DataFrame with missing values handled
        """
        df_filled = df.copy()
        
        numeric_columns = df_filled.select_dtypes(include=[np.number]).columns
        
        if strategy == 'interpolate':
            # Use time-based interpolation for numeric columns
            for col in numeric_columns:
                df_filled[col] = df_filled[col].interpolate(method='time')
        elif strategy == 'forward_fill':
            df_filled[numeric_columns] = df_filled[numeric_columns].fillna(method='ffill')
        elif strategy == 'drop':
            df_filled = df_filled.dropna()
        
        return df_filled
    
    @staticmethod
    def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add derived features to the dataset.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with additional derived features
        """
        df_enhanced = df.copy()
        
        # Time-based features
        df_enhanced['year'] = df_enhanced['date'].dt.year
        df_enhanced['month'] = df_enhanced['date'].dt.month
        df_enhanced['day_of_year'] = df_enhanced['date'].dt.dayofyear
        df_enhanced['season'] = df_enhanced['month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
        })
        
        # Weather-derived features
        if all(col in df_enhanced.columns for col in ['meteo_temp_max', 'meteo_temp_min']):
            df_enhanced['meteo_temp_range'] = (df_enhanced['meteo_temp_max'] - 
                                             df_enhanced['meteo_temp_min'])
        
        if all(col in df_enhanced.columns for col in ['meteo_humedad_max', 'meteo_humedad_min']):
            df_enhanced['meteo_humedad_range'] = (df_enhanced['meteo_humedad_max'] - 
                                                df_enhanced['meteo_humedad_min'])
        
        # Comfort indices
        if all(col in df_enhanced.columns for col in ['meteo_temp_media', 'meteo_humedad_media']):
            # Simple heat index approximation
            df_enhanced['heat_stress_index'] = (df_enhanced['meteo_temp_media'] + 
                                              df_enhanced['meteo_humedad_media'] / 10)
        
        # Reservoir change indicators
        df_enhanced = df_enhanced.sort_values(['embalse_codigo', 'date'])
        df_enhanced['reservoir_change'] = df_enhanced.groupby('embalse_codigo')['embalse_porcentaje'].diff()
        df_enhanced['reservoir_change_7d'] = df_enhanced.groupby('embalse_codigo')['embalse_porcentaje'].diff(7)
        
        return df_enhanced
    
    @staticmethod
    def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate records based on date and reservoir code.
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with duplicates removed
        """
        # Remove duplicates based on date and reservoir code
        df_clean = df.drop_duplicates(subset=['date', 'embalse_codigo'], keep='first')
        
        duplicates_removed = len(df) - len(df_clean)
        if duplicates_removed > 0:
            print(f"Removed {duplicates_removed} duplicate records")
        
        return df_clean
