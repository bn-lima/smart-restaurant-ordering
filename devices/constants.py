from enum import StrEnum

class DeviceFunction(StrEnum):
    CHECKOUT = "Checkout"
    KITCHEN = "Kitchen"

    @classmethod
    def choices(cls):
        return [(category.value, category.name.title()) for category in cls]