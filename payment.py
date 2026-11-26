from abc import ABC, abstractmethod
from typing import Dict, Type

class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self) -> str:
        pass

    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class RazorpayCardPayment(PaymentMethod):
    def __init__(self, card_number: str, **kwargs):
        self.card_number = card_number

    def get_details(self) -> str:
        return f"Razorpay Card ending in {self.card_number[-4:]}"

    def pay(self, amount: float) -> bool:
        print(f"Payment of {amount} made using Razorpay Card")
        return True


class RazorpayUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, **kwargs):
        self.upi_id = upi_id

    def get_details(self) -> str:
        return f"Razorpay UPI ({self.upi_id})"

    def pay(self, amount: float) -> bool:
        print(f"Payment of {amount} made using Razorpay UPI")
        return True


class StripeCardPayment(PaymentMethod):
    def __init__(self, card_number: str, **kwargs):
        self.card_number = card_number

    def get_details(self) -> str:
        return f"Stripe Card [**** **** **** {self.card_number[-4:]}]"

    def pay(self, amount: float) -> bool:
        print(f"Paying {amount} using Stripe Card")
        return True


class StripeUPIPayment(PaymentMethod):
    def __init__(self, upi_id: str, token: str = "", **kwargs):
        self.upi_id = upi_id
        self.token = token

    def get_details(self) -> str:
        return f"Stripe UPI ({self.upi_id})"

    def pay(self, amount: float) -> bool:
        print(f"Paying {amount} using Stripe UPI")
        return True


class FactoryPaymentMethod(ABC):
    factory: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        key = method_type.strip().lower()
        if key not in cls.factory:
            raise ValueError("Invalid payment method")
        return cls.factory[key](**kwargs)


class RazorpayFactory(FactoryPaymentMethod):
    factory = {
        "card": RazorpayCardPayment,
        "upi": RazorpayUPIPayment,
    }


class StripeFactory(FactoryPaymentMethod):
    factory = {
        "card": StripeCardPayment,
        "upi": StripeUPIPayment,
    }


class Aggregator(ABC):
    def __init__(self, name: str, processing_fee: float, factory: Type[FactoryPaymentMethod]):
        self.name = name
        self.processing_fee = processing_fee
        self.factory = factory

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        payment = self.factory.get_payment_object(method_type, **kwargs)
        fee = amount * (self.processing_fee / 100)
        print("Processing fee:", self.processing_fee, "%")
        print("Fee amount:", fee)
        return payment.pay(amount)


class RazorpayAggregator(Aggregator):
    def __init__(self):
        super().__init__("Razorpay", 2.0, RazorpayFactory)


class StripeAggregator(Aggregator):
    def __init__(self):
        super().__init__("Stripe", 2.9, StripeFactory)


class AggregatorFactory:
    factory: Dict[str, Type[Aggregator]] = {
        "stripe": StripeAggregator,
        "razorpay": RazorpayAggregator,
    }

    @classmethod
    def register_aggregator(cls, name: str, aggregator_cls: Type[Aggregator]) -> None:
        cls.factory[name.strip().lower()] = aggregator_cls

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        key = aggregator_name.strip().lower()
        if key not in cls.factory:
            raise ValueError("Invalid aggregator")
        return cls.factory[key]()


def main() -> None:
    print("Multi-Gateway Payment Processing")
    try:
        aggregator_name = input("Select aggregator (stripe/razorpay): ").strip().lower()
        aggregator = AggregatorFactory.get_aggregator_object(aggregator_name)

        method_type = input("Select method (card/upi): ").strip().lower()
        if method_type not in ("card", "upi"):
            raise ValueError("Invalid payment method")

        amount = float(input("Enter amount: "))
        if amount <= 0:
            raise ValueError("Amount must be positive")

        kwargs = {}
        if method_type == "card":
            card_number = input("Enter card number: ").strip()
            if len(card_number) < 4:
                raise ValueError("Invalid card number")
            kwargs["card_number"] = card_number
        else:
            upi_id = input("Enter UPI ID: ").strip()
            if not upi_id:
                raise ValueError("UPI ID cannot be empty")
            kwargs["upi_id"] = upi_id

        result = aggregator.call_get_payment_object(method_type, amount, **kwargs)
        print("Payment successful" if result else "Payment failed")
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("Something went wrong:", e)


if __name__ == "__main__":
    main()