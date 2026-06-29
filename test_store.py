"""Unit-Tests für die Store-Klasse und ihre Magic Methods."""
import pytest

from products import Product
from store import Store


def test_product_in_store():
    """Prüft den in-Operator: Produkt im Store vs. nicht im Store."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    other = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([product])

    assert product in best_buy
    assert other not in best_buy


def test_store_add_combines_products():
    """Prüft +-Operator: zwei Stores ergeben einen neuen kombinierten Store."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    store_a = Store([mac])
    store_b = Store([bose])

    combined = store_a + store_b

    assert len(combined.products) == 2
    assert mac in combined
    assert bose in combined
    assert combined is not store_a
    assert combined is not store_b


def test_store_total_quantity_property():
    """Prüft die total_quantity-Property: Summe aller Produktmengen."""
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    ]
    best_buy = Store(product_list)

    assert best_buy.total_quantity == 600


def test_store_all_products_property():
    """Prüft all_products: nur aktive Produkte werden zurückgegeben."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    best_buy = Store([mac, bose])
    bose.quantity = 0

    assert best_buy.all_products == [mac]


def test_add_product_increases_total_quantity():
    """Prüft, ob add_product die Gesamtmenge erhöht."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([mac, bose])

    best_buy.add_product(pixel)

    assert best_buy.total_quantity == 850
    assert len(best_buy.all_products) == 3


def test_remove_product_decreases_total_quantity():
    """Prüft, ob remove_product ein Produkt entfernt."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = Product("Google Pixel 7", price=500, quantity=250)
    best_buy = Store([mac, bose, pixel])

    best_buy.remove_product(pixel)

    assert pixel not in best_buy
    assert best_buy.total_quantity == 600


def test_order_updates_stock_and_returns_total_price():
    """Prüft eine Bestellung mit mehreren Produkten."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    best_buy = Store([mac, bose])

    total = best_buy.order([(mac, 5), (bose, 10), (mac, 2)])

    assert total == 12650  # 7*1450 + 10*250
    assert mac.quantity == 93
    assert bose.quantity == 490


def test_deactivated_product_not_in_all_products():
    """Prüft, ob ausverkaufte Produkte nicht mehr in all_products sind."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    best_buy = Store([mac, bose])
    bose.quantity = 0

    assert best_buy.all_products == [mac]


def test_order_more_than_available_raises():
    """Prüft, ob eine zu große Bestellung fehlschlägt."""
    mac = Product("MacBook Air M2", price=1450, quantity=100)
    best_buy = Store([mac])

    with pytest.raises(ValueError, match="Nicht genügend Bestand vorhanden."):
        best_buy.order([(mac, 99999)])
