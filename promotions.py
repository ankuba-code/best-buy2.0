"""Definiert abstrakte und konkrete Aktionsklassen für Produkte."""
from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstrakte Basisklasse für alle Rabattaktionen."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """Berechnet den Gesamtpreis nach Anwendung der Aktion."""


class PercentDiscount(Promotion):
    """Prozentualer Rabatt auf den Gesamtpreis."""

    def __init__(self, name: str, percent: int):
        super().__init__(name)
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        return product.price * quantity * (100 - self.percent) / 100


class SecondHalfPrice(Promotion):
    """Zweiter Artikel zum halben Preis."""

    def apply_promotion(self, product, quantity) -> float:
        price = product.price
        pairs = quantity // 2
        singles = quantity % 2
        return pairs * (price + price / 2) + singles * price


class ThirdOneFree(Promotion):
    """Zwei kaufen, einen gratis dazu."""

    def apply_promotion(self, product, quantity) -> float:
        price = product.price
        paid = (quantity // 3) * 2 + (quantity % 3)
        return paid * price
