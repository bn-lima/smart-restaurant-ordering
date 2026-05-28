from enum import StrEnum

class MenuItemCategoryChoices(StrEnum): # Lista de categorias do item

    LANCHES = "Lanches"
    PRATOS_PRINCIPAIS = "Pratos Principais"
    PETISCOS = "Petiscos"
    SOBREMESAS = "Sobremesas"
    BEBIDAS = "Bebidas"
    SALADAS = "Saladas"
    MASSAS = "Massas"
    HAMBURGUERES = "Hambúrgueres"
    PIZZAS = "Pizzas"

    @classmethod
    def choices(cls): # Retorna as categorias formatadas para uso em choices do Django
        return [(category.value, category.name.title().replace("_", " ").replace("Hamburgueres", "Hambúrgueres"))for category in cls]