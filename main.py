"""Startet die Benutzeroberfläche (CLI) für den Best-Buy-Store."""
import products
import promotions
import store


class StoreMenu:
    """Stellt die Menü-Benutzeroberfläche für einen Store bereit."""

    def __init__(self, store_obj):
        """Speichert den Store als Zustand des Menüs."""
        self.store = store_obj
        self.running = True

    @staticmethod
    def display_menu():
        """Gibt das Menü aus."""
        print("""
   Store-Menü
   ----------
1. Alle Produkte im Store auflisten
2. Gesamtmenge im Store anzeigen
3. Bestellung aufgeben
4. Beenden""")

    def list_products(self):
        """Listet alle aktiven Produkte nummeriert auf."""
        active = self.store.all_products
        print("------")
        for i, product in enumerate(active, start=1):
            print(f"{i}. {product.name}, Preis: {product.price}, "
                  f"Menge: {product.quantity}")
        print("------")

    def show_total(self):
        """Zeigt die Gesamtzahl aller Artikel im Store."""
        print(f"Insgesamt {self.store.total_quantity} Artikel im Store")

    def make_order(self):
        """Lässt den Benutzer Produkte auswählen und bestellen."""
        active = self.store.all_products
        self.list_products()
        print(
            "Wenn du die Bestellung abschließen möchtest, "
            "gib einfach nichts ein."
        )

        shopping_list = []
        while True:
            choice = input("Welche Produktnummer möchtest du? ")
            amount = input("Welche Menge möchtest du? ")

            # Leere Eingabe beendet die Bestellung
            if choice == "" or amount == "":
                break

            try:
                # -1, weil die Anzeige bei 1 beginnt, die Liste aber bei 0
                product = active[int(choice) - 1]
                shopping_list.append((product, int(amount)))
                print("Produkt zur Liste hinzugefügt!\n")
            except (ValueError, IndexError):
                print("Fehler beim Hinzufügen des Produkts!\n")

        if shopping_list:
            try:
                total = self.store.order(shopping_list)
                print("********")
                print(f"Bestellung aufgegeben! Gesamtbetrag: {total} €")
            except ValueError as exc:
                print(f"Fehler bei der Bestellung! {exc}")

    def quit(self):
        """Beendet die Menüschleife, indem das Flag umgeschaltet wird."""
        print("Tschüss!")
        self.running = False

    def run(self):
        """Hauptschleife: zeigt das Menü und reagiert auf die Eingabe."""
        while self.running:
            self.display_menu()
            choice = input("Bitte wähle eine Nummer: ")

            if choice == "1":
                self.list_products()
            elif choice == "2":
                self.show_total()
            elif choice == "3":
                self.make_order()
            elif choice == "4":
                self.quit()
            else:
                print("Ungültige Auswahl! Bitte versuche es erneut!")


def main():
    """Erstellt den Standard-Store und startet das Menü."""
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
        products.NonStockedProduct("Windows License", price=125),
        products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1),
    ]

    second_half_price = promotions.SecondHalfPrice("Second Half price!")
    third_one_free = promotions.ThirdOneFree("Third One Free!")
    thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent
    best_buy = store.Store(product_list)
    menu = StoreMenu(best_buy)
    menu.run()


if __name__ == "__main__":
    main()
