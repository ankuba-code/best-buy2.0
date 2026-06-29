"""Definiert die Store-Klasse, die Produkte verwaltet."""
from typing import List

from products import Product


class Store:
    """Verwaltet eine Liste von Produkten und ermöglicht Bestellungen."""

    def __init__(self, product_list=None):
        """Erstellt einen Store. Ohne Argument startet er mit leerer Liste."""
        if product_list is None:
            product_list = []
        self.products = product_list

    def add_product(self, product):
        """Fügt ein Produkt zum Store hinzu."""
        self.products.append(product)

    def remove_product(self, product):
        """Entfernt ein Produkt aus dem Store."""
        self.products.remove(product)

    @property
    def total_quantity(self) -> int:
        """Gibt die Gesamtmenge aller Artikel im Store zurück."""
        total = 0
        for product in self.products:
            total += product.quantity
        return total

    @property
    def all_products(self) -> List[Product]:
        """Gibt alle aktiven Produkte des Stores zurück."""
        return [product for product in self.products if product.active]

    def order(self, shopping_list) -> float:
        """Kauft Produkte aus der (Produkt, Menge)-Liste."""
        total_price = 0.0
        for product, quantity in shopping_list:
            total_price += product.buy(quantity)
        return total_price

    def __contains__(self, product):
        """Prüft, ob ein Produkt im Store vorhanden ist."""
        return product in self.products

    def __add__(self, other):
        """Kombiniert zwei Stores zu einem neuen Store."""
        if not isinstance(other, Store):
            return NotImplemented
        return Store(self.products + other.products)
