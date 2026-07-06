from django.core.management.base import BaseCommand
from devices.models import Device
from django.utils import timezone

class Command(BaseCommand):
    help = "Desbloqueia dispositivos cujo tempo de bloqueio expirou"

    def handle(self, *args, **options):
        
        Device.objects.filter(blocked_until__lte=timezone.now()).update(is_blocked=False, blocked_until=None, login_attempts=0)