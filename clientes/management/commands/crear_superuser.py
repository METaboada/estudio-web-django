from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crear superusuario automáticamente'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@estudio.com'
        password = 'admin123'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(
                self.style.SUCCESS(f'Superusuario "{username}" creado exitosamente')
            )
            self.stdout.write(f'Usuario: {username}')
            self.stdout.write(f'Contraseña: {password}')
        else:
            self.stdout.write(
                self.style.WARNING(f'El superusuario "{username}" ya existe')
            )
