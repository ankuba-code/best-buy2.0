"""Unit-Tests für die Promotion-Klassen und ihre Integration in Product."""
import promotions
from products import NonStockedProduct, Product


def test_percent_discount():
    """Prüft 30%-Rabatt: 2 Artikel à 100 € kosten 140 € statt 200 €."""
    promo = promotions.PercentDiscount("30% off!", percent=30)
    product = Product("Test", price=100, quantity=10)

    assert promo.apply_promotion(product, 2) == 140


def test_second_half_price():
    """Prüft 'Zweiter zum halben Preis' für 1, 2 und 3 Artikel."""
    promo = promotions.SecondHalfPrice("Second Half price!")
    product = Product("Test", price=100, quantity=10)

    assert promo.apply_promotion(product, 1) == 100   # 1 * 100
    assert promo.apply_promotion(product, 2) == 150   # 100 + 50
    assert promo.apply_promotion(product, 3) == 250   # 150 + 100


def test_third_one_free():
    """Prüft 'Dritter gratis': bei 3 zahlt man 2, bei 4 zahlt man 3."""
    promo = promotions.ThirdOneFree("Third One Free!")
    product = Product("Test", price=100, quantity=10)

    assert promo.apply_promotion(product, 3) == 200  # 2 * 100
    assert promo.apply_promotion(product, 4) == 300  # 3 * 100


def test_product_buy_with_promotion():
    """Prüft, ob buy() die Aktion anwendet und den Bestand aktualisiert."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.promotion = promotions.SecondHalfPrice("Second Half price!")

    total = product.buy(2)

    assert total == 2175  # 1450 + 725
    assert product.quantity == 98


def test_non_stocked_product_with_percent_discount():
    """Prüft Rabatt auf ein Produkt ohne Lagerbestand."""
    product = NonStockedProduct("Windows License", price=125)
    product.promotion = promotions.PercentDiscount("30% off!", percent=30)

    total = product.buy(2)

    assert total == 175  # 2 * 125 * 0.7
    assert product.quantity == 0


def test_set_promotion_to_none():
    """Prüft, ob das Entfernen einer Aktion den Normalpreis wiederherstellt."""
    product = Product("Test", price=100, quantity=10)
    product.promotion = promotions.PercentDiscount("30% off!", percent=30)
    product.promotion = None

    assert product.promotion is None
    assert product.buy(2) == 200  # 2 * 100 ohne Rabatt
