# utils/logger.py
"""Logging configuration"""
import logging
import sys


class Logger:
    """Application logger"""

    @staticmethod
    def setup(app_name="Cryptex Gen Pro"):
        """Setup application logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{app_name}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(app_name)