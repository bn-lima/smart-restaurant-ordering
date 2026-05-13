from enum import StrEnum

class DeviceFunction(StrEnum):
    CHECKOUT = "checkout"
    KITCHEN = "kitchen"

    @classmethod
    def choices(cls):
        return [(category.value, category.name.title()) for category in cls]