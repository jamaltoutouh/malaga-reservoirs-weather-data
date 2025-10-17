"""
Exploratory data analysis utilities for reservoir weather data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple
from scipy import stats


class ExploratoryAnalyzer:
    """
    Utility class for performing exploratory data analysis on reservoir weather data.
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize the analyzer with data.
        
        Args:
            data: DataFrame containing reservoir and weather data
        """
        self.data = data.copy()
        self.reservoirs = data['embalse_nombre'].unique() if 'embalse_nombre' in data.columns else []
        
    def seasonal_analysis(self, variable: str, reservoir: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Perform seasonal analysis for a given variable.
        
        Args:
            variable: Variable to analyze
            reservoir: Specific reservoir (None for all)
            
        Returns:
            Dictionary containing seasonal statistics
        """
        df = self.data.copy()
        
        if reservoir:
            df = df[df['embalse_nombre'] == reservoir]
        
        # Add temporal features if not present
        if 'month' not in df.columns:
            df['month'] = df['date'].dt.month
        if 'season' not in df.columns:
            df['season'] = df['month'].map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
            })
        
        results = {}
        
        # Monthly statistics
        monthly_stats = df.groupby('month')[variable].agg(['mean', 'std', 'min', 'max', 'count'])
        results['monthly'] = monthly_stats
        
        # Seasonal statistics
        seasonal_stats = df.groupby('season')[variable].agg(['mean', 'std', 'min', 'max', 'count'])
        results['seasonal'] = seasonal_stats
        
        # Year-over-year comparison
        yearly_seasonal = df.groupby([df['date'].dt.year, 'season'])[variable].mean().unstack()
        results['yearly_seasonal'] = yearly_seasonal
        
        return results
    
    def trend_analysis(self, variable: str, method: str = 'linear') -> Dict[str, any]:
        """
        Analyze long-term trends in a variable.
        
        Args:
            variable: Variable to analyze
            method: Trend analysis method ('linear', 'polynomial', 'mann_kendall')
            
        Returns:
            Dictionary containing trend analysis results
        """
        df = self.data.copy()
        df = df.sort_values('date')
        
        # Create time index for regression
        df['time_index'] = (df['date'] - df['date'].min()).dt.days
        
        results = {}
        
        if method == 'linear':
            # Linear regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(
                df['time_index'], df[variable].dropna()
            )
            
            results['slope'] = slope
            results['intercept'] = intercept
            results['r_squared'] = r_value**2
            results['p_value'] = p_value
            results['std_error'] = std_err
            
            # Annual change rate
            results['annual_change'] = slope * 365.25
            
        elif method == 'mann_kendall':
            # Mann-Kendall trend test (simplified version)
            values = df[variable].dropna().values
            n = len(values)
            
            # Calculate S statistic
            S = 0
            for i in range(n-1):
                for j in range(i+1, n):
                    S += np.sign(values[j] - values[i])
            
            # Variance calculation (simplified)
            var_s = n * (n-1) * (2*n+5) / 18
            
            # Z statistic
            if S > 0:
                z = (S - 1) / np.sqrt(var_s)
            elif S < 0:
                z = (S + 1) / np.sqrt(var_s)
            else:
                z = 0
            
            # P-value (two-tailed)
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))
            
            results['S_statistic'] = S
            results['Z_statistic'] = z
            results['p_value'] = p_value
            results['trend'] = 'increasing' if S > 0 else 'decreasing' if S < 0 else 'no trend'
        
        return results
    
    def reservoir_comparison(self, variables: List[str]) -> pd.DataFrame:
        """
        Compare statistics across reservoirs for multiple variables.
        
        Args:
            variables: List of variables to compare
            
        Returns:
            DataFrame with comparison statistics
        """
        comparison_data = []
        
        for reservoir in self.reservoirs:
            reservoir_data = self.data[self.data['embalse_nombre'] == reservoir]
            
            row = {'reservoir': reservoir}
            
            for var in variables:
                if var in reservoir_data.columns:
                    row[f'{var}_mean'] = reservoir_data[var].mean()
                    row[f'{var}_std'] = reservoir_data[var].std()
                    row[f'{var}_min'] = reservoir_data[var].min()
                    row[f'{var}_max'] = reservoir_data[var].max()
                    row[f'{var}_count'] = reservoir_data[var].count()
            
            comparison_data.append(row)
        
        return pd.DataFrame(comparison_data)
    
    def extreme_events_analysis(self, variable: str, threshold_percentile: float = 95) -> Dict[str, any]:
        """
        Analyze extreme events for a given variable.
        
        Args:
            variable: Variable to analyze
            threshold_percentile: Percentile threshold for extreme events
            
        Returns:
            Dictionary containing extreme events analysis
        """
        df = self.data.copy()
        
        # Calculate threshold
        threshold = df[variable].quantile(threshold_percentile / 100)
        
        # Identify extreme events
        extreme_events = df[df[variable] > threshold]
        
        results = {
            'threshold': threshold,
            'num_extreme_events': len(extreme_events),
            'extreme_percentage': (len(extreme_events) / len(df)) * 100,
            'extreme_events_data': extreme_events,
            'monthly_extreme_counts': extreme_events.groupby(extreme_events['date'].dt.month).size(),
            'yearly_extreme_counts': extreme_events.groupby(extreme_events['date'].dt.year).size()
        }
        
        # Statistics of extreme events
        if len(extreme_events) > 0:
            results['extreme_mean'] = extreme_events[variable].mean()
            results['extreme_max'] = extreme_events[variable].max()
            results['extreme_std'] = extreme_events[variable].std()
        
        return results
    
    def correlation_analysis(self, variables: Optional[List[str]] = None, 
                           method: str = 'pearson') -> pd.DataFrame:
        """
        Perform correlation analysis between variables.
        
        Args:
            variables: List of variables to analyze (None for all numeric)
            method: Correlation method ('pearson', 'spearman', 'kendall')
            
        Returns:
            Correlation matrix DataFrame
        """
        if variables is None:
            variables = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        correlation_matrix = self.data[variables].corr(method=method)
        
        return correlation_matrix
    
    def temporal_patterns(self, variable: str) -> Dict[str, pd.Series]:
        """
        Analyze temporal patterns in a variable.
        
        Args:
            variable: Variable to analyze
            
        Returns:
            Dictionary containing various temporal patterns
        """
        df = self.data.copy()
        df = df.sort_values('date')
        
        patterns = {}
        
        # Daily patterns (day of week)
        patterns['day_of_week'] = df.groupby(df['date'].dt.dayofweek)[variable].mean()
        
        # Monthly patterns
        patterns['monthly'] = df.groupby(df['date'].dt.month)[variable].mean()
        
        # Yearly patterns
        patterns['yearly'] = df.groupby(df['date'].dt.year)[variable].mean()
        
        # Day of year patterns
        patterns['day_of_year'] = df.groupby(df['date'].dt.dayofyear)[variable].mean()
        
        return patterns
    
    def generate_summary_report(self) -> str:
        """
        Generate a comprehensive summary report of the exploratory analysis.
        
        Returns:
            String containing the summary report
        """
        report = []
        report.append("=== EXPLORATORY DATA ANALYSIS SUMMARY ===\n")
        
        # Basic information
        report.append(f"Dataset Shape: {self.data.shape}")
        report.append(f"Date Range: {self.data['date'].min()} to {self.data['date'].max()}")
        report.append(f"Number of Reservoirs: {len(self.reservoirs)}")
        report.append(f"Reservoirs: {', '.join(self.reservoirs)}\n")
        
        # Variable summary
        numeric_vars = self.data.select_dtypes(include=[np.number]).columns
        report.append(f"Numeric Variables ({len(numeric_vars)}):")
        for var in numeric_vars:
            report.append(f"  - {var}")
        report.append("")
        
        # Missing data summary
        missing_data = self.data.isnull().sum()
        missing_vars = missing_data[missing_data > 0]
        if len(missing_vars) > 0:
            report.append("Missing Data:")
            for var, count in missing_vars.items():
                percentage = (count / len(self.data)) * 100
                report.append(f"  - {var}: {count} ({percentage:.1f}%)")
        else:
            report.append("No missing data detected.")
        report.append("")
        
        # Basic statistics for key variables
        key_vars = ['embalse_porcentaje', 'meteo_temp_media', 'meteo_precipitacion']
        key_vars = [var for var in key_vars if var in self.data.columns]
        
        if key_vars:
            report.append("Key Variable Statistics:")
            stats_df = self.data[key_vars].describe()
            report.append(stats_df.to_string())
            report.append("")
        
        return "\n".join(report)
