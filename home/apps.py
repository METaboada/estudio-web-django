from django.apps import AppConfig
from django.db import transaction


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'

    def ready(self):
        # Solo ejecutar en producción y una vez
        import os
        if not os.environ.get('DEBUG', 'True').lower() == 'true':
            try:
                from django.contrib.auth.models import User
                with transaction.atomic():
                    if not User.objects.filter(is_superuser=True).exists():
                        User.objects.create_superuser(
                            username='admin',
                            email='admin@estudio.com',
                            password='admin123'
                        )
                        print("✅ Superusuario creado automáticamente")
            except Exception as e:
                print(f"❌ No se pudo crear superusuario: {e}")
