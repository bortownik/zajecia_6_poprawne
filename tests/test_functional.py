import pytest
from src.manager import Manager
from src.models import Parameters

def test_sum_tenant_settlements_total_due_matches_apartment_cost():
    manager = Manager(Parameters())

    apartment_key = 'apart-polanka'
    year = 2025
    month = 1

    apartment_settlement = manager.get_settlement(apartment_key, year, month)
    assert apartment_settlement is not None

    tenant_settlements = manager.create_tenants_settlements(apartment_settlement)
    assert tenant_settlements is not None

    total_tenant_due = sum(ts.total_due_pln for ts in tenant_settlements)
    assert total_tenant_due == apartment_settlement.total_due_pln


def test_get_debtors_returns_tenants_with_insufficient_transfers():
    manager = Manager(Parameters())

    apartment_key = 'apart-polanka'
    year = 2025
    month = 2 

    debtors = manager.get_debtors(apartment_key, year, month)
    assert debtors is not None
    assert len(debtors) == 3  
    
    debtor_names = {debtor.name for debtor in debtors}
    assert "Jan Nowak" in debtor_names
    assert "Adam Kowalski" in debtor_names
    assert "Ewa Adamska" in debtor_names


def test_get_debtors_returns_none_for_invalid_apartment():
    manager = Manager(Parameters())

    debtors = manager.get_debtors('non-existent-apartment', 2025, 1)
    assert debtors is None


def test_get_debtors_raises_error_for_invalid_month():
    manager = Manager(Parameters())

    with pytest.raises(ValueError, match="Month must be between 1 and 12"):
        manager.get_debtors('apart-polanka', 2025, 13)
    
    with pytest.raises(ValueError, match="Month must be between 1 and 12"):
        manager.get_debtors('apart-polanka', 2025, 0)


def test_find_apartments_without_bills_detects_missing_bills():
    manager = Manager(Parameters())

    apartment_key = 'apart-polanka'
    year = 2025
    month = 2 

    apartments_without_bills = manager.find_apartments_without_bills(apartment_key, year, month)
    assert apartments_without_bills is not None
    assert len(apartments_without_bills) == 1
    assert apartments_without_bills[0].key == apartment_key


def test_find_apartments_without_bills_returns_empty_when_bills_exist():
    manager = Manager(Parameters())

    apartment_key = 'apart-polanka'
    year = 2025
    month = 1  

    apartments_without_bills = manager.find_apartments_without_bills(apartment_key, year, month)
    assert apartments_without_bills is not None
    assert len(apartments_without_bills) == 0


def test_find_apartments_without_bills_returns_none_for_invalid_apartment():
    manager = Manager(Parameters())

    result = manager.find_apartments_without_bills('non-existent-apartment', 2025, 1)
    assert result is None


def test_find_apartments_without_bills_raises_error_for_invalid_month():
    manager = Manager(Parameters())

    with pytest.raises(ValueError, match="Month must be between 1 and 12"):
        manager.find_apartments_without_bills('apart-polanka', 2025, 13)
    
    with pytest.raises(ValueError, match="Month must be between 1 and 12"):
        manager.find_apartments_without_bills('apart-polanka', 2025, 0)

