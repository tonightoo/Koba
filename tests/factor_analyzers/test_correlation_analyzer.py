import unittest
import pandas as pd
from src.interfaces import IPipelineStage, PipelineContext
from src.factor_analyzers.correlation_analyzer import CorrelationAnalyzer


class TestCorrelationAnalyzer(unittest.TestCase):
    def setUp(self):
        config = {
            'threshold': 0.7,
            'target_column': 'temperature',
            'feature_columns': [],
            'data_types': {}
        }
        self.analyzer: IPipelineStage = CorrelationAnalyzer(config)

    def test_calculate_correlation_scores_correctly(self):
        data = pd.DataFrame({
            'temperature': [15, 18, 20, 22, 25, 28, 30, 32, 35, 38],
            'sales_of_icecream': [200, 250, 280, 320, 400, 450, 500, 530, 600, 650],
            'sales_of_hot_coffee': [500, 450, 400, 380, 300, 250, 200, 150, 100, 80],
            'not_related_data': [4, 1, 2, 5, 3, 5, 1, 5, 4, 3]
        })

        context = PipelineContext(data)
        result_context = self.analyzer.execute(context)

        correlation_result = result_context.analysis_results['correlation_result']
        has_high_correlation = correlation_result['has_high_correlation']

        is_high_correlation_ice = correlation_result['data'].loc[
                                        (correlation_result['data']['target_column'] == 'temperature') &
                                        (correlation_result['data']['compare_column'] == 'sales_of_icecream'),
                                        'is_high_correlation'
                                    ].values[0]

        is_high_correlation_coffee = correlation_result['data'].loc[
                                        (correlation_result['data']['target_column'] == 'temperature') &
                                        (correlation_result['data']['compare_column'] == 'sales_of_hot_coffee'),
                                        'is_high_correlation'
                                    ].values[0]

        is_high_correlation_not = correlation_result['data'].loc[
                                        (correlation_result['data']['target_column'] == 'temperature') &
                                        (correlation_result['data']['compare_column'] == 'not_related_data'),
                                        'is_high_correlation'
                                    ].values[0]

        self.assertTrue(has_high_correlation)
        self.assertTrue(is_high_correlation_ice)
        self.assertTrue(is_high_correlation_coffee)
        self.assertFalse(is_high_correlation_not)

    def test_nominal(self):
        data = pd.DataFrame({
            'temperature': [15, 18, 20, 22, 25, 28, 30, 32, 35, 38],
            'sales_of_icecream': [200, 250, 280, 320, 400, 450, 500, 530, 600, 650],
            'sales_of_hot_coffee': [500, 450, 400, 380, 300, 250, 200, 150, 100, 80],
            'not_related_data': [4, 1, 2, 5, 3, 5, 1, 5, 4, 3],
            'name': ['Alex', 'Bill', 'Choco', 'Deluxe', 'Edge', 'Final', 'Giant', 'Hex', 'Ion', 'Jhon']
        })

        context = PipelineContext(data)
        result_context = self.analyzer.execute(context)

        correlation_result = result_context.analysis_results['correlation_result']
        compare_columns = correlation_result['data']['compare_column'].tolist()
        self.assertNotIn('name', compare_columns)


    def test_ordinal(self):
        data = pd.DataFrame({
            'temperature': [15, 18, 20, 22, 25, 28, 30, 32, 35, 38],
            'satisfaction_rank': [1, 2, 2, 3, 3, 4, 4, 5, 5, 5],
            'danger_level': ['Low', 'Low', 'Low', 'Mid', 'Mid', 'Mid', 'High', 'High', 'High', 'High']
        })

        context = PipelineContext(data)
        
        config = {
            'threshold': 0.7,
            'target_column': 'temperature',
            'feature_columns': ['satisfaction_rank', 'danger_level'],
            'data_types': {
                'danger_level': 'ordinal'
            }
        }

        self.analyzer = CorrelationAnalyzer(config)
        
        result_context = self.analyzer.execute(context)
        correlation_result = result_context.analysis_results['correlation_result']['data']

        # expected data with spearman analysis
        expected_satisfaction_corr = data['temperature'].corr(data['satisfaction_rank'], method='spearman')
        
        danger_codes = data['danger_level'].astype('category').cat.codes
        expected_danger_corr = data['temperature'].corr(danger_codes, method='spearman')

        actual_satisfaction = correlation_result.loc[correlation_result['compare_column'] == 'satisfaction_rank', 'correlation_value'].values[0]
        actual_danger = correlation_result.loc[correlation_result['compare_column'] == 'danger_level', 'correlation_value'].values[0]

        self.assertAlmostEqual(actual_satisfaction, expected_satisfaction_corr)
        self.assertAlmostEqual(actual_danger, expected_danger_corr)

    def test_continuous(self):
        data = pd.DataFrame({
            'temperature': [15, 18, 20, 22, 25, 28, 30, 32, 35, 38],
            'sales_of_icecream': [200, 250, 280, 320, 400, 450, 500, 530, 600, 650], 
            'sales_of_hot_coffee': [500, 450, 400, 380, 300, 250, 200, 150, 100, 80],
            'not_related_data': [4, 1, 2, 5, 3, 5, 1, 5, 4, 3]                      
        })

        context = PipelineContext(data)
        
        result_context = self.analyzer.execute(context)
        correlation_result = result_context.analysis_results['correlation_result']['data']

        expected_icecream_corr = data['temperature'].corr(data['sales_of_icecream'], method='pearson')
        expected_coffee_corr = data['temperature'].corr(data['sales_of_hot_coffee'], method='pearson')

        actual_icecream = correlation_result.loc[correlation_result['compare_column'] == 'sales_of_icecream', 'correlation_value'].values[0]
        actual_coffee = correlation_result.loc[correlation_result['compare_column'] == 'sales_of_hot_coffee', 'correlation_value'].values[0]

        self.assertAlmostEqual(actual_icecream, expected_icecream_corr)
        self.assertAlmostEqual(actual_coffee, expected_coffee_corr)

        self.assertTrue(actual_icecream > 0.8)
        self.assertTrue(actual_coffee < -0.8)


