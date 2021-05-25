# Copyright (c) 2013, ac and contributors
# For license information, please see license.txt

# import frappe
from pprint import pprint

import frappe
from frappe import _


def execute(filters=None):
    company = ''

    from_date = filters.get('from_date')
    to_date = filters.get('to_date')
    date_range = [from_date, to_date]

    columns = [
        {
            'fieldname': 'account',
            'label': _('Account'),
            'fieldtype': 'Link',
            'options': 'Account',
            'width': '200px',
        },
        {
            'fieldname': 'balance',
            'lable': _('Balance'),
            'fieldtype': 'Currency',
            'width': '100px',
        }
    ]
    # accounts = get_accounts(company)
    # balances = get_balances(accounts, date_range)
    # data = balances

    data = get_data(date_range, None, 'Asset', 'Debit')
    pprint(data)

    return columns, data


def get_accounts(company=None, root_type=None):
    filters = {}

    if root_type:
        filters = {'account_type': ['=', root_type]}
    fields = ['name', 'parent_account', 'lft', 'account_type', 'account_type', 'is_group']
    # fields = ['*']

    accounts = frappe.get_all('Account', fields=fields, filters=filters, order_by='lft')
    return accounts


def get_account_balance(account, date_range):
    query = f'''
    SELECT
        SUM(debit) - SUM(credit)
    FROM
        `tabGL Entry`
    WHERE
        account="{account}" and is_cancelled=0 and
        posting_date >= "{date_range[0]}" and posting_date <= "{date_range[1]}"
    '''
    result = frappe.db.sql(query)
    return result[0][0]


def get_balances(accounts, date_range):
    for account in accounts:
        balance = get_account_balance(account['name'], date_range)
        account['balance'] = balance

    return accounts
