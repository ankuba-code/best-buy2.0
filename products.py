"""Definiert die Product-Klasse für den Store."""


class Product:
    """Repräsentiert einen Produkttyp im Geschäft (z. B. MacBook Air M2)."""

    def __init__(self, name: str, price: float, quantity: int):
        """Erstellt ein Produkt und prüft die Eingaben auf Gültigkeit."""
        if not name:
            raise ValueError("Der Name darf nicht leer sein.")
        if price < 0:
            raise ValueError("Der Preis darf nicht negativ sein.")
        if quantity < 0:
            raise ValueError("Die Menge darf nicht negativ sein.")

        self.name = name
        self.price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None

    @property
    def quantity(self) -> int:
        """Gibt die aktuelle Menge zurück."""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Setzt die Menge. Erreicht sie 0, wird das Produkt deaktiviert."""
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    @property
    def active(self) -> bool:
        """Gibt zurück, ob das Produkt aktiv ist."""
        return self._active

    @property
    def promotion(self):
        """Gibt die aktuelle Aktion zurück."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion):
        """Weist eine Aktion zu oder entfernt sie mit None."""
        self._promotion = promotion

    def activate(self):
        """Aktiviert das Produkt."""
        self._active = True

    def deactivate(self):
        """Deaktiviert das Produkt."""
        self._active = False

    def __str__(self):
        """Gibt eine String-Repräsentation des Produkts zurück."""
        result = (
            f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"
        )
        if self.promotion:
            result += f"\nPromotion: {self.promotion.name}"
        return result

    def __lt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    def __gt__(self, other):
        if not isinstance(other, Product):
            return NotImplemented
        return self.price > other.price

    def _get_total_price(self, quantity) -> float:
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity

    def buy(self, quantity) -> float:
        """Kauft eine Menge und gibt den Preis zurück."""
        if quantity <= 0:
            raise ValueError("Die Kaufmenge muss größer als 0 sein.")
        if not self.active:
            raise ValueError(
                "Das Produkt ist nicht aktiv und kann nicht gekauft werden."
            )
        if quantity > self.quantity:
            raise ValueError("Nicht genügend Bestand vorhanden.")

        total_price = self._get_total_price(quantity)
        self.quantity = self.quantity - quantity
        return total_price


class NonStockedProduct(Product):
    """Produkt ohne Lagerbestand (z. B. Software-Lizenz)."""

    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)

    @Product.quantity.setter
    def quantity(self, quantity):
        """Menge bleibt immer 0; das Produkt wird nicht deaktiviert."""
        self._quantity = 0

    def __str__(self):
        return f"{super().__str__()}\nNon-stocked product"

    def buy(self, quantity) -> float:
        if quantity <= 0:
            raise ValueError("Die Kaufmenge muss größer als 0 sein.")
        if not self.active:
            raise ValueError(
                "Das Produkt ist nicht aktiv und kann nicht gekauft werden."
            )
        return self._get_total_price(quantity)


class LimitedProduct(Product):
    """Produkt mit maximalem Kauflimit pro Bestellung."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        if maximum <= 0:
            raise ValueError(
                "Das Maximum pro Bestellung muss größer als 0 sein."
            )
        self.maximum = maximum
        super().__init__(name, price, quantity)

    def __str__(self):
        return f"{super().__str__()}\nMaximum per order: {self.maximum}"

    def buy(self, quantity) -> float:
        if quantity > self.maximum:
            raise ValueError(
                "Die Kaufmenge überschreitet das Maximum pro Bestellung."
            )
        return super().buy(quantity)
