"""
Data loading utilities for reservoir and weather data.
"""

import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Optional, Union


class ReservoirDataLoader:
    """
    Utility class for loading reservoir and weather data from CSV files.
    """
    
    def __init__(self, data_path: str = "data/reservoir-weather"):
        """
        Initialize the data loader.
        
        Args:
            data_path: Path to the data directory
        """
        self.data_path = Path(data_path)
        self.reservoirs = self._get_available_reservoirs()
    
    def _get_available_reservoirs(self) -> List[str]:
        """Get list of available reservoir names from CSV files."""
        csv_files = list(self.data_path.glob("*.csv"))
        # Exclude test files
        reservoirs = [f.stem for f in csv_files if f.stem != "test"]
        return sorted(reservoirs)
    
    def load_single_reservoir(self, reservoir_name: str) -> pd.DataFrame:
        """
        Load data for a single reservoir.
        
        Args:
            reservoir_name: Name of the reservoir (e.g., 'CASASOLA')
            
        Returns:
            DataFrame with reservoir and weather data
        """
        file_path = self.data_path / f"{reservoir_name}.csv"
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def load_all_reservoirs(self) -> Dict[str, pd.DataFrame]:
        """
        Load data for all available reservoirs.
        
        Returns:
            Dictionary mapping reservoir names to DataFrames
        """
        data = {}
        for reservoir in self.reservoirs:
            try:
                data[reservoir] = self.load_single_reservoir(reservoir)
            except FileNotFoundError as e:
                print(f"Warning: {e}")
        return data
    
    def load_combined_data(self) -> pd.DataFrame:
        """
        Load and combine data from all reservoirs into a single DataFrame.
        
        Returns:
            Combined DataFrame with all reservoir data
        """
        all_data = []
        for reservoir in self.reservoirs:
            try:
                df = self.load_single_reservoir(reservoir)
                all_data.append(df)
            except FileNotFoundError as e:
                print(f"Warning: {e}")
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        else:
            return pd.DataFrame()
    
    def get_date_range(self, reservoir_name: Optional[str] = None) -> tuple:
        """
        Get the date range for a specific reservoir or all reservoirs.
        
        Args:
            reservoir_name: Name of the reservoir, or None for all reservoirs
            
        Returns:
            Tuple of (start_date, end_date)
        """
        if reservoir_name:
            df = self.load_single_reservoir(reservoir_name)
            return df['date'].min(), df['date'].max()
        else:
            df = self.load_combined_data()
            return df['date'].min(), df['date'].max()
    
    def get_reservoir_info(self) -> pd.DataFrame:
        """
        Get basic information about all reservoirs.
        
        Returns:
            DataFrame with reservoir codes, names, and data availability
        """
        info_data = []
        for reservoir in self.reservoirs:
            try:
                df = self.load_single_reservoir(reservoir)
                info = {
                    'reservoir_name': reservoir,
                    'reservoir_code': df['embalse_codigo'].iloc[0],
                    'start_date': df['date'].min(),
                    'end_date': df['date'].max(),
                    'total_records': len(df),
                    'avg_capacity_percentage': df['embalse_porcentaje'].mean()
                }
                info_data.append(info)
            except Exception as e:
                print(f"Error processing {reservoir}: {e}")
        
        return pd.DataFrame(info_data)
