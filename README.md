# Best Buy 2

CLI-Store in Python mit Produkten, Rabattaktionen und Bestellverwaltung.

## Features

- **Produkte:** `Product`, `NonStockedProduct`, `LimitedProduct`
- **Rabatte:** `PercentDiscount`, `SecondHalfPrice`, `ThirdOneFree`
- **Store:** Bestellungen, `in`-Operator, `+`-Operator zum Kombinieren
- **CLI-Menü:** Produkte anzeigen, Bestand prüfen, Bestellungen aufgeben

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ausführung

```bash
# Interaktives Menü starten
python main.py

# Alle Tests ausführen
python -m pytest -v
```

## Projektstruktur

| Datei | Beschreibung |
|-------|--------------|
| `products.py` | Produktklassen mit Properties und `__str__` |
| `promotions.py` | Rabattaktionen (abstrakte Basisklasse) |
| `store.py` | Store-Verwaltung und Bestellungen |
| `main.py` | CLI-Menü |
| `test_product.py` | Tests für Produkte |
| `test_promotions.py` | Tests für Rabattaktionen |
| `test_store.py` | Tests für den Store |

## Tests

```bash
python -m pytest test_product.py    # Produkte
python -m pytest test_promotions.py # Rabatte
python -m pytest test_store.py      # Store
```
