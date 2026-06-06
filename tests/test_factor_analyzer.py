import unittest
import pandas as pd
from src.interfaces import IFactorAnalyzer
from src.factor_analyzer import CorrelationAnalyzer


class TestCorrelationAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = CorrelationAnalyzer()

    def test_calculate_correlation_scores_correctly(self):


