from enum import StrEnum

class CartStatusChoices(StrEnum):
    OPEN = "open"
    PAID = "paid"
    CANCELED = "canceled"

    @classmethod
    def choices(cls):
        return [(category.value, category.name.title()) for category in cls]