# Copyright (c) 2021, ac and Contributors
# See license.txt

# import frappe
import unittest

from frappe import ValidationError
from tests.utils import get_or_create_doc


class TestJournalEntry(unittest.TestCase):
	def setUp(self) -> None:
		params = {
			'doctype': 'Journal Entry Item',
			'key': '',

		}
		accounting_entries = get_or_create_doc(fields=params)

		self.json = {
			'doctype': 'Journal Entry',
			'key': 'naming_series',
			'naming_series': 'ACC-JRN-TEST-0001',
			'total_debit': 100,
			'total_credit': 20,
			'accounting_entries': ''
		}

	def aa_test_app_should_raise_error_when_difference_is_not_zero(self):
		get_or_create_doc(fields=self.json)

		self.assertRaises(ValidationError, get_or_create_doc, fields=self.json)
