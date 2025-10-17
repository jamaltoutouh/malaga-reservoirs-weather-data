# Reservoir-Weather Combined Dataset

This directory contains the complete dataset combining reservoir water levels with meteorological variables for seven major reservoirs in Málaga, Spain.

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

## File Information

### Individual Reservoir Files
Each reservoir has its own CSV file named after the reservoir:

| File | Reservoir | Code | Records | Date Range |
|------|-----------|------|---------|------------|
| `CASASOLA.csv` | Casasola | S19 | ~8,300 | 2002-2024 |
| `CONCEPCION.csv` | Concepción | S20 | ~8,600 | 2000-2024 |
| `CONDE_DE_GUADALHORCE.csv` | Conde de Guadalhorce | S21 | ~8,600 | 2000-2024 |
| `GUADALHORCE.csv` | Guadalhorce | S30 | ~8,600 | 2000-2024 |
| `GUADALTEBA.csv` | Guadalteba | S22 | ~8,600 | 2000-2024 |
| `LIMONERO.csv` | Limonero | S23 | ~8,600 | 2000-2024 |
| `VINUELA.csv` | Viñuela | S24 | ~8,600 | 2000-2024 |

### Data Sources
- **Reservoir Data**: Spanish water management authorities
- **Meteorological Data**: AEMET (Spanish Meteorological Agency)
- **Weather Stations**: 2-3 stations per reservoir area, data averaged for robustness

## Usage Examples

### Load Single Reservoir
```python
import pandas as pd

# Load Casasola reservoir data
casasola = pd.read_csv('CASASOLA.csv')
casasola['date'] = pd.to_datetime(casasola['date'])
print(f"Data shape: {casasola.shape}")
print(f"Date range: {casasola['date'].min()} to {casasola['date'].max()}")
```

### Load All Reservoirs
```python
import pandas as pd
from pathlib import Path

# Load all reservoir files
reservoir_files = Path('.').glob('*.csv')
reservoir_files = [f for f in reservoir_files if f.name != 'test.csv']

all_data = []
for file in reservoir_files:
    df = pd.read_csv(file)
    df['date'] = pd.to_datetime(df['date'])
    all_data.append(df)

combined_data = pd.concat(all_data, ignore_index=True)
print(f"Combined dataset shape: {combined_data.shape}")
```

## Data Quality Notes

### Completeness
- Most reservoirs have complete data from 2000-2024
- Casasola starts from 2002
- Weather data averaged from multiple stations for reliability

### Known Issues
- Some floating-point precision artifacts may be present
- Occasional missing values handled through interpolation
- Weather station changes over time may introduce minor discontinuities

### Validation
- Temperature consistency: min ≤ mean ≤ max
- Humidity ranges: 0-100%
- Reservoir percentages: 0-100%
- Physical range checks for all meteorological variables

## Research Applications

This dataset enables analysis of:
- **Water Resource Management**: Reservoir capacity planning and optimization
- **Climate Impact Studies**: Long-term trends and climate change effects
- **Seasonal Analysis**: Seasonal patterns in water availability
- **Weather-Water Relationships**: Precipitation, temperature, and evaporation effects
- **Drought Studies**: Extreme events and water scarcity analysis
- **Regional Variations**: Comparative analysis across different reservoirs

## Citation

If you use this dataset in your research, please cite:
```
TO-DO
```

## License

This dataset is provided under the MIT License. See the main project LICENSE file for details.

## Contact

For questions about the dataset or to report issues, please open an issue in the main project repository.
