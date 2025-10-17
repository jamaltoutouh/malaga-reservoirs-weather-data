# Málaga Reservoirs Weather Data Analysis

## Overview

This project analyzes water reservoir data combined with meteorological variables for seven major reservoirs in Málaga, Spain. The dataset spans from 2000 to 2024 and includes reservoir water levels alongside comprehensive weather measurements.

## Dataset Description

### Reservoirs Included
- **CASASOLA** (S19)
- **CONCEPCION** (S20)
- **CONDE DE GUADALHORCE** (S21)
- **GUADALHORCE** (S30)
- **GUADALTEBA** (S22)
- **LIMONERO** (S23)
- **VIÑUELA** (S24)

### Data Structure

Each CSV file contains daily observations with the following variables:

#### Reservoir Data
- `date`: Date of observation (YYYY-MM-DD)
- `embalse_codigo`: Reservoir code (e.g., S19, S30)
- `embalse_nombre`: Reservoir name
- `embalse_provincia`: Province (MALAGA)
- `embalse_reserva`: Water reserve (cubic hectometers)
- `embalse_porcentaje`: Water level percentage of total capacity

#### Meteorological Data
- `meteo_temp_max`: Maximum daily temperature (°C)
- `meteo_temp_min`: Minimum daily temperature (°C)
- `meteo_temp_media`: Average daily temperature (°C)
- `meteo_humedad_max`: Maximum daily humidity (%)
- `meteo_humedad_min`: Minimum daily humidity (%)
- `meteo_humedad_media`: Average daily humidity (%)
- `meteo_vel_viento`: Average wind speed (m/s)
- `meteo_vel_viento_max`: Maximum wind speed (m/s)
- `meteo_dir_viento`: Wind direction (degrees)
- `meteo_radiacion`: Solar radiation (MJ/m²)
- `meteo_precipitacion`: Precipitation (mm)

#### Quality Control
- `num_estaciones_promediadas`: Number of weather stations averaged
- `estaciones_usadas`: Weather stations used for measurements

## Project Structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── reservoir/           # Original reservoir data only
│   └── reservoir-weather/   # Combined reservoir and weather data
├── src/
│   ├── __init__.py
│   ├── data_processing/
│   │   ├── __init__.py
│   │   ├── loader.py        # Data loading utilities
│   │   ├── cleaner.py       # Data cleaning functions
│   │   └── validator.py     # Data validation
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── exploratory.py   # Exploratory data analysis
│   │   ├── correlation.py   # Correlation analysis
│   │   └── time_series.py   # Time series analysis
│   └── visualization/
│       ├── __init__.py
│       ├── plotting.py      # General plotting functions
│       └── dashboard.py     # Interactive dashboards
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_reservoir_analysis.ipynb
│   ├── 03_weather_patterns.ipynb
│   └── 04_correlation_analysis.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py
│   ├── test_analysis.py
│   └── test_visualization.py
├── docs/
│   ├── methodology.md
│   └── results.md
└── output/
    ├── figures/
    ├── reports/
    └── processed_data/
```

## Getting Started

### Prerequisites
- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- jupyter
- scipy
- plotly (for interactive visualizations)

### Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd malaga-reservoirs-weather-data
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Launch Jupyter Notebook:
```bash
jupyter notebook
```

### Usage

1. Start with the exploratory data analysis notebook: `notebooks/01_data_exploration.ipynb`
2. Explore reservoir-specific patterns: `notebooks/02_reservoir_analysis.ipynb`
3. Analyze weather patterns: `notebooks/03_weather_patterns.ipynb`
4. Study correlations: `notebooks/04_correlation_analysis.ipynb`

## Data Quality Notes

- Weather data is averaged from multiple meteorological stations (2-3 stations per reservoir)
- Some data points may contain floating-point precision artifacts
- Data coverage varies by reservoir (2000-2024 for most, 2002-2024 for some)
- Missing values are handled in the data processing pipeline

## Research Questions

This dataset enables investigation of:
- Seasonal patterns in reservoir water levels
- Impact of meteorological variables on water storage
- Correlation between precipitation and reservoir filling
- Temperature and evaporation effects
- Regional variations across different reservoirs
- Long-term trends in water availability

## Contributing

Please read `docs/methodology.md` for details on our methodology and contribution guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Students name