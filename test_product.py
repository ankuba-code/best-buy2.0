"""Unit-Tests für die Product-Klasse und ihre Unterklassen."""
import pytest

from products import LimitedProduct, NonStockedProduct, Product


def test_create_normal_product():
    """Prüft, ob ein Produkt mit gültigen Werten korrekt erstellt wird."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.active is True


@pytest.mark.parametrize(
    "name, price, quantity",
    [
        ("", 1450, 100),              # leerer Name
        ("MacBook Air M2", -10, 100),  # negativer Preis
    ],
)
def test_create_with_invalid_details_raises(name, price, quantity):
    """Prüft, ob ungültige Eingaben beim Erstellen eine ValueError auslösen."""
    with pytest.raises(ValueError):
        Product(name, price=price, quantity=quantity)


def test_product_becomes_inactive_at_zero_quantity():
    """Prüft, ob ein Produkt nach dem Ausverkauf deaktiviert wird."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    product.buy(100)

    assert product.quantity == 0
    assert product.active is False


def test_buy_changes_quantity_and_returns_correct_price():
    """Prüft, ob buy() den Bestand reduziert und den Preis liefert."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    total = product.buy(10)

    assert total == 14500  # 10 * 1450
    assert product.quantity == 90


def test_buy_more_than_available_raises():
    """Prüft, ob ein Kauf über den verfügbaren Bestand hinaus fehlschlägt."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    with pytest.raises(ValueError, match="Nicht genügend Bestand vorhanden."):
        product.buy(101)


def test_non_stocked_product_starts_with_zero_quantity():
    """Prüft, ob NonStockedProduct mit Menge 0 startet und aktiv bleibt."""
    product = NonStockedProduct("Windows License", price=125)

    assert product.quantity == 0
    assert product.active is True


def test_non_stocked_product_buy_keeps_quantity_at_zero():
    """Prüft, ob der Kauf bei NonStockedProduct die Menge bei 0 hält."""
    product = NonStockedProduct("Windows License", price=125)

    total = product.buy(3)

    assert total == 375  # 3 * 125
    assert product.quantity == 0
    assert product.active is True


def test_limited_product_buy_within_maximum():
    """Prüft, ob ein Kauf innerhalb des Limits erfolgreich ist."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    total = product.buy(1)

    assert total == 10
    assert product.quantity == 249


def test_limited_product_buy_exceeds_maximum_raises():
    """Prüft, ob ein Kauf über dem Maximum pro Bestellung fehlschlägt."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    with pytest.raises(
        ValueError,
        match="Die Kaufmenge überschreitet das Maximum pro Bestellung.",
    ):
        product.buy(2)


def test_product_str():
    """Prüft die String-Darstellung eines normalen Produkts (__str__)."""
    product = Product("MacBook Air M2", price=1450, quantity=100)

    assert str(product) == "MacBook Air M2, Price: 1450, Quantity: 100"


def test_non_stocked_product_str():
    """Prüft, ob NonStockedProduct als solches in __str__ erkennbar ist."""
    product = NonStockedProduct("Windows License", price=125)

    assert "Non-stocked product" in str(product)


def test_limited_product_str():
    """Prüft, ob das Kauflimit in __str__ angezeigt wird."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)

    assert "Maximum per order: 1" in str(product)


def test_product_price_comparison():
    """Prüft den Preisvergleich zwischen Produkten mit > und <."""
    cheap = Product("Cheap", price=100, quantity=10)
    expensive = Product("Expensive", price=500, quantity=10)

    assert cheap < expensive
    assert expensive > cheap
