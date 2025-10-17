"""
Data validation utilities for reservoir weather data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


class DataValidator:
    """
    Utility class for validating reservoir weather data quality.
    """
    
    @staticmethod
    def check_data_completeness(df: pd.DataFrame) -> Dict[str, float]:
        """
        Check data completeness for all columns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with column names and completeness percentages
        """
        completeness = {}
        for col in df.columns:
            non_null_count = df[col].notna().sum()
            completeness[col] = (non_null_count / len(df)) * 100
        
        return completeness
    
    @staticmethod
    def check_temporal_consistency(df: pd.DataFrame) -> Dict[str, any]:
        """
        Check temporal consistency of the data.
        
        Args:
            df: Input DataFrame with 'date' column
            
        Returns:
            Dictionary with temporal consistency metrics
        """
        df_sorted = df.sort_values('date')
        date_diffs = df_sorted['date'].diff()
        
        results = {
            'date_range': (df['date'].min(), df['date'].max()),
            'total_days': (df['date'].max() - df['date'].min()).days,
            'unique_dates': df['date'].nunique(),
            'duplicate_dates': len(df) - df['date'].nunique(),
            'missing_days': 0,  # Will be calculated if needed
            'median_gap_days': date_diffs.dt.days.median(),
            'max_gap_days': date_diffs.dt.days.max()
        }
        
        return results
    
    @staticmethod
    def validate_weather_consistency(df: pd.DataFrame) -> Dict[str, List[int]]:
        """
        Validate weather data consistency (e.g., min <= mean <= max).
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with inconsistency indices for each validation rule
        """
        inconsistencies = {}
        
        # Temperature consistency: min <= mean <= max
        if all(col in df.columns for col in ['meteo_temp_min', 'meteo_temp_media', 'meteo_temp_max']):
            temp_inconsistent = df[
                (df['meteo_temp_min'] > df['meteo_temp_media']) |
                (df['meteo_temp_media'] > df['meteo_temp_max'])
            ].index.tolist()
            inconsistencies['temperature_order'] = temp_inconsistent
        
        # Humidity consistency: min <= mean <= max
        if all(col in df.columns for col in ['meteo_humedad_min', 'meteo_humedad_media', 'meteo_humedad_max']):
            humidity_inconsistent = df[
                (df['meteo_humedad_min'] > df['meteo_humedad_media']) |
                (df['meteo_humedad_media'] > df['meteo_humedad_max'])
            ].index.tolist()
            inconsistencies['humidity_order'] = humidity_inconsistent
        
        # Wind speed consistency: average <= max
        if all(col in df.columns for col in ['meteo_vel_viento', 'meteo_vel_viento_max']):
            wind_inconsistent = df[
                df['meteo_vel_viento'] > df['meteo_vel_viento_max']
            ].index.tolist()
            inconsistencies['wind_speed_order'] = wind_inconsistent
        
        return inconsistencies
    
    @staticmethod
    def check_reservoir_consistency(df: pd.DataFrame) -> Dict[str, List[int]]:
        """
        Check reservoir data consistency.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with reservoir inconsistency indices
        """
        inconsistencies = {}
        
        # Check if percentage is consistent with absolute values (if we had capacity data)
        # For now, just check percentage is within reasonable bounds
        percentage_issues = df[
            (df['embalse_porcentaje'] < 0) | (df['embalse_porcentaje'] > 100)
        ].index.tolist()
        inconsistencies['percentage_out_of_bounds'] = percentage_issues
        
        # Check for extreme jumps in reservoir levels (>20% in one day)
        df_sorted = df.sort_values(['embalse_codigo', 'date'])
        df_sorted['percentage_change'] = df_sorted.groupby('embalse_codigo')['embalse_porcentaje'].diff()
        extreme_changes = df_sorted[
            df_sorted['percentage_change'].abs() > 20
        ].index.tolist()
        inconsistencies['extreme_percentage_changes'] = extreme_changes
        
        return inconsistencies
    
    @staticmethod
    def generate_quality_report(df: pd.DataFrame) -> Dict[str, any]:
        """
        Generate comprehensive data quality report.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary with complete quality assessment
        """
        report = {}
        
        # Basic statistics
        report['basic_stats'] = {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Data completeness
        report['completeness'] = DataValidator.check_data_completeness(df)
        
        # Temporal consistency
        report['temporal_consistency'] = DataValidator.check_temporal_consistency(df)
        
        # Weather consistency
        report['weather_inconsistencies'] = DataValidator.validate_weather_consistency(df)
        
        # Reservoir consistency
        report['reservoir_inconsistencies'] = DataValidator.check_reservoir_consistency(df)
        
        # Outlier detection (simple IQR method)
        report['outliers'] = DataValidator._detect_outliers(df)
        
        return report
    
    @staticmethod
    def _detect_outliers(df: pd.DataFrame, threshold: float = 1.5) -> Dict[str, int]:
        """
        Detect outliers using IQR method.
        
        Args:
            df: Input DataFrame
            threshold: IQR multiplier threshold
            
        Returns:
            Dictionary with outlier counts per column
        """
        outliers = {}
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                
                outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                outliers[col] = outlier_count
        
        return outliers
    
    @staticmethod
    def print_quality_summary(report: Dict[str, any]) -> None:
        """
        Print a human-readable quality summary.
        
        Args:
            report: Quality report from generate_quality_report()
        """
        print("=== DATA QUALITY REPORT ===\n")
        
        # Basic stats
        stats = report['basic_stats']
        print(f"Total Records: {stats['total_records']:,}")
        print(f"Total Columns: {stats['total_columns']}")
        print(f"Memory Usage: {stats['memory_usage_mb']:.2f} MB\n")
        
        # Completeness
        print("=== DATA COMPLETENESS ===")
        completeness = report['completeness']
        for col, pct in completeness.items():
            if pct < 100:
                print(f"{col}: {pct:.1f}%")
        print()
        
        # Inconsistencies
        print("=== INCONSISTENCIES ===")
        weather_issues = report['weather_inconsistencies']
        reservoir_issues = report['reservoir_inconsistencies']
        
        total_issues = sum(len(issues) for issues in weather_issues.values())
        total_issues += sum(len(issues) for issues in reservoir_issues.values())
        
        if total_issues > 0:
            print(f"Total inconsistent records: {total_issues}")
            for issue_type, indices in weather_issues.items():
                if indices:
                    print(f"  {issue_type}: {len(indices)} records")
            for issue_type, indices in reservoir_issues.items():
                if indices:
                    print(f"  {issue_type}: {len(indices)} records")
        else:
            print("No major inconsistencies detected")
        print()
        
        # Outliers
        print("=== OUTLIERS ===")
        outliers = report['outliers']
        for col, count in outliers.items():
            if count > 0:
                print(f"{col}: {count} outliers")
        print()
