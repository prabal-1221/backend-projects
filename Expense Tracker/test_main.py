from main import main
from unittest.mock import patch

def test_add_expense(monkeypatch):
    with patch('main.ExpenseDao.add_expense') as mock_add_expense:
        monkeypatch.setattr('sys.argv', ['main.py', 'add', '--description', 'Lunch', '--amount', '20'])

        main()

        mock_add_expense.assert_called_once_with('Lunch', 20)

def test_summary_expense(monkeypatch):
    with patch('main.ExpenseDao.summary_expense') as mock_summary_expense:
        monkeypatch.setattr('sys.argv', ['main.py', 'summary'])

        main()

        mock_summary_expense.assert_called_once_with()

def test_summary_expense_month(monkeypatch):
    with patch('main.ExpenseDao.summary_expense_month') as mock_summary_expense_month:
        monkeypatch.setattr('sys.argv', ['main.py', 'summary', '--month', '1'])

        main()

        mock_summary_expense_month.assert_called_once_with(1)

def test_delete_expense(monkeypatch):
    with patch('main.ExpenseDao.delete_expense') as mock_delete_expense:

        monkeypatch.setattr('sys.argv', ['main.py', 'delete', '--id', '1'])

        main()

        mock_delete_expense.assert_called_once_with(1)

def test_update_expense(monkeypatch):
    with patch('main.ExpenseDao.update_expense') as mock_update_expense:
        monkeypatch.setattr('sys.argv', ['main.py', 'update', '--id', '1', '--description', 'Dinner', '--amount', '30'])

        main()

        mock_update_expense.assert_called_once_with(1, 'Dinner', 30)

