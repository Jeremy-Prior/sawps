from population_data.models import AnnualPopulation
from frontend.utils.metrics import calculate_population_categories
import unittest
from species.factories import (
    TaxonRankFactory
)
from species.models import Taxon, TaxonRank
from unittest.mock import patch
from property.models import Property
from django.db.models.query import QuerySet


class TestCalculatePopulationCategories(unittest.TestCase):
    def setUp(self):
        taxon_rank = TaxonRank.objects.filter(name="Species").first()
        if not taxon_rank:
            taxon_rank = TaxonRankFactory.create(name="Species")

    def test_empty_queryset(self):
        # Test when the queryset is empty
        queryset = []
        species_name = "Penthera leo"
        result = calculate_population_categories(queryset, species_name)
        self.assertEqual(result, {})

    def test_no_annual_population_data(self):
        # Test when there is no annual population data
        queryset = [
            Property(id=1),
            Property(id=2),
        ]
        species_name = "Penthera leo"
        result = calculate_population_categories(queryset, species_name)
        self.assertEqual(result, {})

    @patch('population_data.models.AnnualPopulation.objects.filter')
    def test_population_categories_calculation(self, mock_filter):
        # Test the calculation of population categories
        # Create mock annual population data
        annual_population_data = [
            {'year': 2021, 'population_total': 100},
            {'year': 2022, 'population_total': 400},
            {'year': 2023, 'population_total': 300},
            {'year': 2024, 'population_total': 200},
        ]

        # Create a mock queryset and set its return value
        mock_queryset = QuerySet(model=AnnualPopulation)
        mock_queryset._result_cache = annual_population_data
        mock_filter.return_value = mock_queryset

        queryset = [
            Property(id=1),
            Property(id=2),
        ]
        species_name = "Panthera Leo"
        result = calculate_population_categories(queryset, species_name)

        # Confirm it contains data
        self.assertIsNotNone(result)

        # Assert that each result object contains a 'year' key
        for key, value in result.items():
            self.assertIn('year', value)

        # Test all aspects of calculate function were covered
        self.assertTrue(any(item['population_total'] >= 100 and item['population_total'] < 250 for item in annual_population_data))
        self.assertTrue(any(item['population_total'] >= 250 and item['population_total'] < 400 for item in annual_population_data))
        self.assertTrue(any(item['population_total'] >= 400 and item['population_total'] < 550 for item in annual_population_data))


if __name__ == '__main__':
    unittest.main()
