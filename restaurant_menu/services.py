from .models import MenuItem

def get_menu_item_by_id(id):
    try:
        menu_item = MenuItem.objects.get(id=id)
    except MenuItem.DoesNotExist:
        return None
    return menu_item