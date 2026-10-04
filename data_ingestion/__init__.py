"""
Data Ingestion Package for Downtown San Diego Homeless Population Analysis (Assignment 10).
Provides modular pipelines for external data sources:
- 311 Get It Done Service Requests
- NOAA / Open-Meteo Climatological Signals
- Major Events (MLB Padres, Comic-Con, Holidays)
- Macroeconomic Indicators (FRED Unemployment, CPI, Zillow ZORI)
- Shelter Capacity & Policy Regimes
"""

from .base import BaseIngestionPipeline
from .aligner import MultiSourceAligner
from .validator import DataQualityValidator

__all__ = ["BaseIngestionPipeline", "MultiSourceAligner", "DataQualityValidator"]
