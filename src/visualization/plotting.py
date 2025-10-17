"""
General plotting functions for reservoir weather data visualization.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Tuple, Dict


class ReservoirPlotter:
    """
    Utility class for creating visualizations of reservoir and weather data.
    """
    
    def __init__(self, style: str = 'whitegrid', palette: str = 'husl'):
        """
        Initialize the plotter with custom styling.
        
        Args:
            style: Seaborn style ('whitegrid', 'darkgrid', 'white', 'dark', 'ticks')
            palette: Color palette for plots
        """
        sns.set_style(style)
        sns.set_palette(palette)
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
    
    @staticmethod
    def plot_reservoir_levels(df: pd.DataFrame, 
                            reservoirs: Optional[List[str]] = None,
                            figsize: Tuple[int, int] = (15, 8)) -> plt.Figure:
        """
        Plot reservoir water levels over time.
        
        Args:
            df: DataFrame with reservoir data
            reservoirs: List of reservoir names to plot (None for all)
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        if reservoirs is None:
            reservoirs = df['embalse_nombre'].unique()
        
        for reservoir in reservoirs:
            reservoir_data = df[df['embalse_nombre'] == reservoir]
            if not reservoir_data.empty:
                ax.plot(reservoir_data['date'], 
                       reservoir_data['embalse_porcentaje'],
                       label=reservoir, linewidth=2, alpha=0.8)
        
        ax.set_xlabel('Date')
        ax.set_ylabel('Water Level (%)')
        ax.set_title('Reservoir Water Levels Over Time')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_seasonal_patterns(df: pd.DataFrame, 
                             variable: str = 'embalse_porcentaje',
                             figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Plot seasonal patterns for a given variable.
        
        Args:
            df: DataFrame with data
            variable: Variable to analyze
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        # Add month column if not present
        if 'month' not in df.columns:
            df['month'] = df['date'].dt.month
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        axes = axes.ravel()
        
        # Monthly boxplot
        sns.boxplot(data=df, x='month', y=variable, ax=axes[0])
        axes[0].set_title(f'Monthly Distribution of {variable}')
        axes[0].set_xlabel('Month')
        
        # Yearly trend
        yearly_avg = df.groupby(df['date'].dt.year)[variable].mean()
        axes[1].plot(yearly_avg.index, yearly_avg.values, marker='o')
        axes[1].set_title(f'Yearly Average {variable}')
        axes[1].set_xlabel('Year')
        axes[1].grid(True, alpha=0.3)
        
        # Monthly average by reservoir
        if 'embalse_nombre' in df.columns:
            monthly_by_reservoir = df.groupby(['embalse_nombre', 'month'])[variable].mean().unstack()
            sns.heatmap(monthly_by_reservoir, ax=axes[2], cmap='viridis', cbar_kws={'label': variable})
            axes[2].set_title(f'Monthly {variable} by Reservoir')
        
        # Distribution
        df[variable].hist(bins=30, ax=axes[3], alpha=0.7)
        axes[3].set_title(f'Distribution of {variable}')
        axes[3].set_xlabel(variable)
        axes[3].set_ylabel('Frequency')
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_weather_correlation_matrix(df: pd.DataFrame,
                                      figsize: Tuple[int, int] = (12, 10)) -> plt.Figure:
        """
        Plot correlation matrix of weather variables.
        
        Args:
            df: DataFrame with weather data
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        # Select weather columns
        weather_cols = [col for col in df.columns if col.startswith('meteo_')]
        weather_cols.extend(['embalse_porcentaje', 'embalse_reserva'])
        
        # Filter existing columns
        weather_cols = [col for col in weather_cols if col in df.columns]
        
        correlation_matrix = df[weather_cols].corr()
        
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(correlation_matrix, 
                   annot=True, 
                   cmap='RdBu_r', 
                   center=0,
                   square=True,
                   ax=ax,
                   fmt='.2f')
        
        ax.set_title('Weather Variables Correlation Matrix')
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_precipitation_vs_reservoir(df: pd.DataFrame,
                                      reservoir_name: str,
                                      figsize: Tuple[int, int] = (15, 6)) -> plt.Figure:
        """
        Plot precipitation vs reservoir levels for a specific reservoir.
        
        Args:
            df: DataFrame with data
            reservoir_name: Name of the reservoir
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        reservoir_data = df[df['embalse_nombre'] == reservoir_name].copy()
        reservoir_data = reservoir_data.sort_values('date')
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
        
        # Precipitation
        ax1.bar(reservoir_data['date'], reservoir_data['meteo_precipitacion'], 
               alpha=0.7, color='steelblue', width=1)
        ax1.set_ylabel('Precipitation (mm)')
        ax1.set_title(f'{reservoir_name} - Precipitation and Water Level')
        ax1.grid(True, alpha=0.3)
        
        # Reservoir level
        ax2.plot(reservoir_data['date'], reservoir_data['embalse_porcentaje'], 
                color='darkgreen', linewidth=2)
        ax2.set_ylabel('Water Level (%)')
        ax2.set_xlabel('Date')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_temperature_trends(df: pd.DataFrame,
                              figsize: Tuple[int, int] = (15, 8)) -> plt.Figure:
        """
        Plot temperature trends across all reservoirs.
        
        Args:
            df: DataFrame with temperature data
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Temperature range over time
        axes[0, 0].fill_between(df['date'], df['meteo_temp_min'], df['meteo_temp_max'], 
                               alpha=0.3, label='Temperature Range')
        axes[0, 0].plot(df['date'], df['meteo_temp_media'], color='red', 
                       linewidth=1, label='Average Temperature')
        axes[0, 0].set_title('Daily Temperature Range')
        axes[0, 0].set_ylabel('Temperature (°C)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Monthly temperature averages
        monthly_temp = df.groupby(df['date'].dt.month)['meteo_temp_media'].mean()
        axes[0, 1].plot(monthly_temp.index, monthly_temp.values, marker='o', linewidth=2)
        axes[0, 1].set_title('Average Monthly Temperature')
        axes[0, 1].set_xlabel('Month')
        axes[0, 1].set_ylabel('Temperature (°C)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Temperature distribution by season
        if 'season' not in df.columns:
            df['season'] = df['date'].dt.month.map({
                12: 'Winter', 1: 'Winter', 2: 'Winter',
                3: 'Spring', 4: 'Spring', 5: 'Spring',
                6: 'Summer', 7: 'Summer', 8: 'Summer',
                9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
            })
        
        sns.boxplot(data=df, x='season', y='meteo_temp_media', ax=axes[1, 0])
        axes[1, 0].set_title('Temperature Distribution by Season')
        
        # Yearly temperature trend
        yearly_temp = df.groupby(df['date'].dt.year)['meteo_temp_media'].mean()
        axes[1, 1].plot(yearly_temp.index, yearly_temp.values, marker='o', linewidth=2)
        axes[1, 1].set_title('Yearly Average Temperature Trend')
        axes[1, 1].set_xlabel('Year')
        axes[1, 1].set_ylabel('Temperature (°C)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_reservoir_comparison(df: pd.DataFrame,
                                metric: str = 'embalse_porcentaje',
                                figsize: Tuple[int, int] = (15, 10)) -> plt.Figure:
        """
        Compare reservoirs across different metrics.
        
        Args:
            df: DataFrame with reservoir data
            metric: Metric to compare
            figsize: Figure size tuple
            
        Returns:
            Matplotlib figure object
        """
        reservoirs = df['embalse_nombre'].unique()
        
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Average values comparison
        avg_values = df.groupby('embalse_nombre')[metric].mean().sort_values(ascending=False)
        axes[0, 0].bar(range(len(avg_values)), avg_values.values)
        axes[0, 0].set_xticks(range(len(avg_values)))
        axes[0, 0].set_xticklabels(avg_values.index, rotation=45, ha='right')
        axes[0, 0].set_title(f'Average {metric} by Reservoir')
        axes[0, 0].set_ylabel(metric)
        
        # Box plot comparison
        sns.boxplot(data=df, x='embalse_nombre', y=metric, ax=axes[0, 1])
        axes[0, 1].set_xticklabels(axes[0, 1].get_xticklabels(), rotation=45, ha='right')
        axes[0, 1].set_title(f'{metric} Distribution by Reservoir')
        
        # Time series comparison (subset for clarity)
        for reservoir in reservoirs[:5]:  # Show only first 5 reservoirs
            reservoir_data = df[df['embalse_nombre'] == reservoir]
            axes[1, 0].plot(reservoir_data['date'], reservoir_data[metric], 
                           label=reservoir, alpha=0.8, linewidth=1)
        axes[1, 0].set_title(f'{metric} Over Time (Selected Reservoirs)')
        axes[1, 0].set_xlabel('Date')
        axes[1, 0].set_ylabel(metric)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Seasonal patterns
        if 'month' not in df.columns:
            df['month'] = df['date'].dt.month
        
        seasonal_data = df.groupby(['embalse_nombre', 'month'])[metric].mean().unstack()
        sns.heatmap(seasonal_data, ax=axes[1, 1], cmap='viridis', 
                   cbar_kws={'label': metric})
        axes[1, 1].set_title(f'Monthly {metric} by Reservoir')
        
        plt.tight_layout()
        return fig
