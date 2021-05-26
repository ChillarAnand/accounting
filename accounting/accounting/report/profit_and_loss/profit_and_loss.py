# Copyright (c) 2013, ac and contributors
# For license information, please see license.txt

from pprint import pprint

import frappe
from frappe import _


def execute(filters=None):
    filter_type = filters.get('filter_type')
    if filter_type == 'Date Range':
        from_date = filters.get('from_date')
        to_date = filters.get('to_date')
    elif filter_type == 'Fiscal Year':
        fiscal_year = filters.get('fiscal_year')
        fiscal_year = frappe.get_all('Fiscal Year', fields=['*'], filters={'year_name': fiscal_year})
        from_date = fiscal_year[0].start_date
        to_date = fiscal_year[0].end_date

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
            'label': _('Balance'),
            'fieldtype': 'Currency',
            'width': '100px',
        }
    ]

    accounts = []
    accounts.extend(get_accounts(account_type='Income'))
    accounts.extend(get_accounts(account_type='Expense'))

    for account in accounts:
        account['account'] = account['name']

    accounts = indent_accounts(accounts)

    accounts = get_balances(accounts, date_range)
    accounts = propagate_balances(accounts)

    accounts.append(get_profit_and_loss(accounts))
    data = accounts

    return columns, data


def get_profit_and_loss(accounts):
    asset = next((account for account in accounts if account['name'] == 'Income'))
    liability = next((account for account in accounts if account['name'] == 'Expense'))
    balance = asset['balance'] - liability['balance']

    pnl = {
        'account': 'Provisional Profit/Loss',
        'balance': balance,
    }
    return pnl


def get_children(accounts, account):
    children = []
    for _account in accounts:
        if _account['parent_account'] == account['name']:
            children.append(_account)
    return children


def propagate_balances(accounts):
    for account in accounts:
        account['balance'] = get_cumulative_balance(accounts, account)
        # if account['balance'] is None:
        #     account['balance'] = get_cumulative_balance(accounts, account)

    return accounts


def get_accounts(account_type=None):
    filters = {}

    if account_type:
        filters = {'account_type': ['=', account_type]}
    fields = ['name', 'parent_account', 'lft', 'account_type', 'account_type', 'is_group']

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


def get_cumulative_balance(accounts, account):
    children = get_children(accounts, account)

    if not children:
        return account['balance']

    for child in children:
        if child['balance'] is None:
            child['balance'] = get_cumulative_balance(accounts, child)

    balance = 0
    for child in children:
        if child['balance']:
            balance += child['balance']

    # balance += get_account_balance(account)

    return balance


def get_balances(accounts, date_range):
    for account in accounts:

        # if account['is_group']:
        #     account['balance'] = 0
        #     continue

        balance = get_account_balance(account['name'], date_range)
        if balance and balance < 0:
            balance = abs(balance)
        account['balance'] = balance

    return accounts


def indent_accounts(accounts):
    for account in accounts:
        depth = 0
        current_account = account
        parent = current_account['parent_account']
        while parent is not None:
            depth += 1
            current_account = frappe.get_list(
                'Account', fields=['name', 'parent_account'],
                filters={'name': parent}
            )
            parent = current_account[0]['parent_account']

        account.indent = depth

    return accounts
