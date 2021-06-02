# Copyright (c) 2021, ac and Contributors
# See license.txt

import unittest

from frappe import ValidationError
from tests.utils import get_or_create_doc


class TestFiscalYear(unittest.TestCase):
	def setUp(self) -> None:
		self.json = {
			'doctype': 'Fiscal Year',
			# 'key': 'year_name',
			'year_name': '2021-2023',
			'start_date': '2021-04-01',
			'end_date': '2022-03-31',
		}

	def test_create_fiscal_year(self):
		created, fiscal_year = get_or_create_doc(fields=self.json)
		assert fiscal_year

	def test_app_should_raise_exception_for_invalid_range(self):
		self.json['year_name'] = '2222-2223'
		self.json['start_date'] = '2222-01-01'
		self.assertRaises(ValidationError, get_or_create_doc, fields=self.json)
