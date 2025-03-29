# metrics.py

import numpy as np
from typing import List, Dict, Union
from dataclasses import dataclass

@dataclass
class MetricsResult:
    min: float
    max: float
    median: float
    std_dev: float
    percentile_90: float
    percentile_95: float
    percentile_99: float

class MetricsCalculator:
    @staticmethod
    def calculate_metrics(data: List[Union[int, float]]) -> MetricsResult:
        """
        Calculate statistical metrics from a list of numerical values.
        
        Args:
            data: List of numerical values to analyze
            
        Returns:
            MetricsResult object containing all calculated metrics
            
        Raises:
            ValueError: If input data is empty or contains non-numeric values
        """
        if not data:
            raise ValueError("Cannot calculate metrics for empty dataset")

        try:
            np_data = np.array(data, dtype=float)
        except (ValueError, TypeError):
            raise ValueError("Input data must contain only numerical values")

        return MetricsResult(
            min=float(np.min(np_data)),
            max=float(np.max(np_data)),
            median=float(np.median(np_data)),
            std_dev=float(np.std(np_data)),
            percentile_90=float(np.percentile(np_data, 90)),
            percentile_95=float(np.percentile(np_data, 95)),
            percentile_99=float(np.percentile(np_data, 99))
        )

    @staticmethod
    def format_metrics(metrics: MetricsResult) -> Dict[str, float]:
        """
        Format metrics result into a dictionary with rounded values.
        
        Args:
            metrics: MetricsResult object to format
            
        Returns:
            Dictionary containing formatted metric values
        """
        return {
            "min": round(metrics.min, 2),
            "max": round(metrics.max, 2),
            "median": round(metrics.median, 2),
            "std_dev": round(metrics.std_dev, 2),
            "p90": round(metrics.percentile_90, 2),
            "p95": round(metrics.percentile_95, 2),
            "p99": round(metrics.percentile_99, 2)
        }

    @classmethod
    def process_metrics(cls, data: List[Union[int, float]]) -> Dict[str, float]:
        """
        Calculate and format metrics in one step.
        
        Args:
            data: List of numerical values to analyze
            
        Returns:
            Dictionary containing formatted metric values
        """
        metrics = cls.calculate_metrics(data)
        return cls.format_metrics(metrics)
