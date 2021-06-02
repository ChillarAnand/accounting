# Copyright (c) 2021, ac and Contributors
# See license.txt

import unittest

import frappe
from frappe.exceptions import ValidationError


class TestJournalEntry(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		cls.doctype = 'Journal Entry'
	
	def test_journal_entry_validation_errors(self):
		with self.assertRaises(ValidationError):
			entries = [{
				'account': 'SBI',
				'party': 'Frappe',
				'debit': 100.00,
			}]
			self.create_journal_entry(entries=entries)
			
		with self.assertRaises(ValidationError):
			entries = [
				{
					'account': 'SBI',
					'party': 'Frappe',
					'debit': 100.00,
				},
				{
					'account': 'SBI',
					'party': 'Frappe',
					'debit': 100.00,
				},
			]
			self.create_journal_entry(entries=entries)
			
	@classmethod
	def create_journal_entry(cls, entries=None):
		journal = frappe.new_doc(cls.doctype)
		if not entries:
			entries = [
				{
					'account': 'SBI',
					'party': 'Frappe',
					'debit': 100.00,
				},
				{
					'account': 'HDFC',
					'party': 'Frappe',
					'credit': 100.00,
				}
			]
		journal.set('accounting_entries', entries)
		journal.insert()
		
		return journal
