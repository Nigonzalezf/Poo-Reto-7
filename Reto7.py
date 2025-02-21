import json
from collections import deque, namedtuple
from typing import List, Dict, Any

MenuItemTuple = namedtuple('MenuItemTuple', ['name', 'price'])

class MenuItem:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def calculate_total_price(self, quantity: int = 1) -> float:
        return self.price * quantity


class Beverage(MenuItem):
    def __init__(self, name: str, price: float, is_alcoholic: bool = False):
        super().__init__(name, price)
        self.is_alcoholic = is_alcoholic


class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, is_shared: bool = True):
        super().__init__(name, price)
        self.is_shared = is_shared


class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, is_vegetarian: bool = False):
        super().__init__(name, price)
        self.is_vegetarian = is_vegetarian


class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item: MenuItem, quantity: int = 1):
        self.items.append((item, quantity))

    def calculate_total(self) -> float:
        total = sum(item.calculate_total_price(quantity) for item, quantity in self.items)
        return total

    def apply_discount(self, percentage: float) -> float:
        total = self.calculate_total()
        discount = total * (percentage / 100)
        return total - discount

    def print_order(self):
        print("Detalles del pedido:")
        for item, quantity in self.items:
            print(f"{quantity}x {item.name} - ${item.price:.2f} cada uno")
        print(f"Total: ${self.calculate_total():.2f}")

    def save_menu(self, menu: Dict[str, Any], filename: str):
        with open(filename, 'w') as f:
            json.dump(menu, f)

    def load_menu(self, filename: str) -> Dict[str, Any]:
        with open(filename, 'r') as f:
            return json.load(f)
        
    def update_menu(self, menu: Dict[str, Any], item_name: str, new_price: float):
        if item_name in menu:
            menu[item_name]['price'] = new_price
        else:
            print(f"Item {item_name} no encontrado en el menu")

    def delete_menu_item(self, menu: Dict[str, Any], item_name: str):
        if item_name in menu:
            del menu[item_name]
        else:
            print(f"Item {item_name} no encontrado en el menu")
        

class Payment:
    def __init__(self, order: Order):
        self.order = order
        self.amount_paid = 0.0

    def process_payment(self, amount: float, method: str):
        if amount < self.order.calculate_total():
            print("El monto pagado es menor que el total del pedido.")
            return False
        
        self.amount_paid = amount
        print(f"Pago de ${amount:.2f} procesado con éxito mediante {method}.")
        return True

    def print_receipt(self):
        print("Recibo de Pago:")
        self.order.print_order()
        print(f"Monto pagado: ${self.amount_paid:.2f}")
        if self.amount_paid > self.order.calculate_total():
            change = self.amount_paid - self.order.calculate_total()
            print(f"Cambio: ${change:.2f}")
        elif self.amount_paid < self.order.calculate_total():
            print("Pago incompleto.")
        else:
            print("Pago exacto.")


class Restaurant:
    def __init__ (self):
        self.orders = deque()

    def add_order(self, order: Order):
        self.orders.append(order)

    def process_next_order(self):
        if self.orders:
            order = self.orders.popleft()
            order.print_order()
            return order
        else:
            print("No hay pedidos en la cola")
            return None

if __name__ == "__main__":
    menu = {
        "Cerveza": {"price": 5.0, "type": "Beverage"},
        "Ensalada": {"price": 7.5, "type": "Appetizer"},
        "Pizza": {"price": 12.0, "type": "MainCourse"},
    }

restaurant = Restaurant()

order = Order()
order.add_item(Beverage("Cerveza", 5.0), quantity = 2)
order.add_item(Appetizer("Ensalada", 7.5), quantity = 1)
order.add_item(MainCourse("Pizza", 12.0), quantity = 1)

restaurant.add_order(order)

processed_order = restaurant.process_next_order()

if processed_order:
    payment = Payment(processed_order)
    payment.process_payment(30.0, "Tarjeta de credito")
    payment.print_receipt()


     
