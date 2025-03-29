# graph.py

import matplotlib
# Set the backend to 'Agg' before importing pyplot
# otherwise: matplotlib is trying to create a GUI window in a non-main thread
# which throws error: Terminating app due to uncaught exception 'NSInternalInconsistencyException', reason: 'NSWindow drag regions should only be invalidated on the Main Thread!'
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union, Optional
from datetime import datetime
import os

class ResponseTimeGrapher:
    def __init__(self):
        # Set style for better-looking graphs
        # plt.style.use('seaborn')

        # Use a standard style that's guaranteed to be available
        plt.style.use('bmh')  # Alternative options: 'classic', 'default', 'fast'
        
        # Set some default styling
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = 'white'
        plt.rcParams['grid.alpha'] = 0.3
        plt.rcParams['grid.color'] = '#cccccc'
        
    def create_scatter_plot(
        self,
        response_times: List[Union[int, float]],
        title: str = "Response Times Over Time",
        output_dir: str = "graphs",
        filename: Optional[str] = None
    ) -> str:
        """
        Create a scatter plot of response times over time.
        
        Args:
            response_times: List of response time values
            title: Title for the graph
            output_dir: Directory to save the graph
            filename: Optional filename for the graph (default: timestamp)
            
        Returns:
            str: Path to the saved graph file
            
        Raises:
            ValueError: If response_times is empty or contains invalid values
        """
        if not response_times:
            raise ValueError("No response times provided for plotting")

        try:
            '''
            # Create figure and axis
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Create x-axis values (sample numbers)
            x = np.arange(len(response_times))
            
            # Create scatter plot
            ax.scatter(x, response_times, alpha=0.6, c='blue', s=50)
            
            # Add trend line
            z = np.polyfit(x, response_times, 1)
            p = np.poly1d(z)
            ax.plot(x, p(x), "r--", alpha=0.8, label='Trend')
            
            # Calculate statistics for annotations
            mean = np.mean(response_times)
            median = np.median(response_times)
            
            # Add horizontal lines for mean and median
            ax.axhline(y=mean, color='g', linestyle='--', alpha=0.5, label=f'Mean: {mean:.3f}s')
            ax.axhline(y=median, color='y', linestyle='--', alpha=0.5, label=f'Median: {median:.3f}s')
            
            # Customize the plot
            ax.set_title(title, pad=20)
            ax.set_xlabel('Sample Number')
            ax.set_ylabel('Response Time (seconds)')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Add timestamp annotation
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            plt.figtext(0.99, 0.01, f'Generated: {timestamp}', 
                       ha='right', va='bottom', 
                       fontsize=8, style='italic')
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename if not provided
            if filename is None:
                filename = f"response_times_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Ensure filename has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            # Save the plot
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filepath
            '''
            # Create figure with subplots
            fig = plt.figure(figsize=(15, 10))
            fig.patch.set_facecolor('white')
            
            # Scatter plot
            ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
            ax1.set_facecolor('white')
            x = np.arange(len(response_times))
            ax1.scatter(x, response_times, alpha=0.6, c='#1f77b4', s=50)
            ax1.set_title('Response Times Over Time', fontsize=11, fontweight='bold')
            ax1.set_xlabel('Sample Number', fontsize=10)
            ax1.set_ylabel('Response Time (seconds)', fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Add trend line to scatter plot
            z = np.polyfit(x, response_times, 1)
            p = np.poly1d(z)
            ax1.plot(x, p(x), "r--", alpha=0.8, label='Trend')
            ax1.legend(frameon=True, facecolor='white', framealpha=1)
            
            # Histogram
            ax2 = plt.subplot2grid((2, 2), (1, 0))
            ax2.set_facecolor('white')
            ax2.hist(response_times, bins=30, alpha=0.7, color='#1f77b4')
            ax2.set_title('Response Time Distribution', fontsize=11, fontweight='bold')
            ax2.set_xlabel('Response Time (seconds)', fontsize=10)
            ax2.set_ylabel('Frequency', fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            # Box plot
            ax3 = plt.subplot2grid((2, 2), (1, 1))
            ax3.set_facecolor('white')
            ax3.boxplot(response_times, vert=True)
            ax3.set_title('Response Time Box Plot', fontsize=11, fontweight='bold')
            ax3.set_ylabel('Response Time (seconds)', fontsize=10)
            ax3.grid(True, alpha=0.3)
            
            # Add main title
            plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
            
            # Add timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            plt.figtext(0.99, 0.01, f'Generated: {timestamp}', 
                       ha='right', va='bottom', 
                       fontsize=8, style='italic')
            
            # Adjust layout
            plt.tight_layout()
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename if not provided
            if filename is None:
                filename = f"response_time_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Ensure filename has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            # Save the plot
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            return filepath
        
        except Exception as e:
            plt.close()  # Ensure figure is closed in case of error
            raise ValueError(f"Error creating scatter plot: {str(e)}")

    def create_multi_plot(
        self,
        response_times: List[Union[int, float]],
        title: str = "Response Time Analysis",
        output_dir: str = "graphs",
        filename: Optional[str] = None
    ) -> str:
        """
        Create a multi-plot analysis of response times including scatter plot,
        histogram, and box plot.
        
        Args:
            response_times: List of response time values
            title: Title for the graph
            output_dir: Directory to save the graph
            filename: Optional filename for the graph (default: timestamp)
            
        Returns:
            str: Path to the saved graph file
        """
        if not response_times:
            raise ValueError("No response times provided for plotting")

        try:
            # Create figure with subplots
            fig = plt.figure(figsize=(15, 10))
            
            # Scatter plot
            ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
            x = np.arange(len(response_times))
            ax1.scatter(x, response_times, alpha=0.6, c='blue', s=50)
            ax1.set_title('Response Times Over Time')
            ax1.set_xlabel('Sample Number')
            ax1.set_ylabel('Response Time (seconds)')
            ax1.grid(True, alpha=0.3)
            
            # Add trend line to scatter plot
            z = np.polyfit(x, response_times, 1)
            p = np.poly1d(z)
            ax1.plot(x, p(x), "r--", alpha=0.8, label='Trend')
            ax1.legend()
            
            # Histogram
            ax2 = plt.subplot2grid((2, 2), (1, 0))
            ax2.hist(response_times, bins=30, alpha=0.7, color='blue')
            ax2.set_title('Response Time Distribution')
            ax2.set_xlabel('Response Time (seconds)')
            ax2.set_ylabel('Frequency')
            ax2.grid(True, alpha=0.3)
            
            # Box plot
            ax3 = plt.subplot2grid((2, 2), (1, 1))
            ax3.boxplot(response_times, vert=True)
            ax3.set_title('Response Time Box Plot')
            ax3.set_ylabel('Response Time (seconds)')
            ax3.grid(True, alpha=0.3)
            
            # Add main title
            plt.suptitle(title, fontsize=16, y=1.02)
            
            # Add timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            plt.figtext(0.99, 0.01, f'Generated: {timestamp}', 
                       ha='right', va='bottom', 
                       fontsize=8, style='italic')
            
            # Adjust layout
            plt.tight_layout()
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate filename if not provided
            if filename is None:
                filename = f"response_time_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Ensure filename has .png extension
            if not filename.endswith('.png'):
                filename += '.png'
            
            # Save the plot
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filepath
            
        except Exception as e:
            plt.close()  # Ensure figure is closed in case of error
            raise ValueError(f"Error creating multi-plot: {str(e)}")
