from django.apps import AppConfig
from django.db import transaction


class ClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'

    def ready(self):
        # Solo ejecutar en producción y una vez
        import os
        if not os.environ.get('DEBUG', 'True').lower() == 'true':
            try:
                from .models import Cliente
                with transaction.atomic():
                    if not Cliente.objects.exists():
                        clientes_prueba = [
                            {
                                'nombre': 'EMPRESA EJEMPLO S.A.',
                                'cuit': '30-12345678-9',
                                'domicilio': 'Av. Corrientes 1234, CABA',
                                'clave_fiscal': 'clave123',
                                'activo': True
                            },
                            {
                                'nombre': 'CONSULTORA ABC S.R.L.',
                                'cuit': '30-87654321-0',
                                'domicilio': 'San Martín 567, Buenos Aires',
                                'clave_fiscal': 'clave456',
                                'clave_ciudad': 'claveciudad123',
                                'activo': True
                            },
                            {
                                'nombre': 'SERVICIOS INTEGRALES DEL SUR',
                                'cuit': '27-98765432-1',
                                'domicilio': 'Belgrano 890, La Plata',
                                'clave_arba': 'arbaclave789',
                                'activo': True
                            },
                            {
                                'nombre': 'IMPORTADORA NORTE',
                                'cuit': '30-11223344-5',
                                'domicilio': 'Rivadavia 2345, Rosario',
                                'clave_fiscal': 'fiscal789',
                                'activo': False
                            }
                        ]
                        
                        for cliente_data in clientes_prueba:
                            Cliente.objects.create(**cliente_data)
                        
                        print("✅ Clientes de prueba creados automáticamente")
            except Exception as e:
                print(f"❌ No se pudieron crear clientes: {e}")
