from django.core.management.base import BaseCommand
from clientes.models import Cliente


class Command(BaseCommand):
    help = 'Crear clientes de prueba'

    def handle(self, *args, **options):
        # Datos de clientes de prueba
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
                'activo': False
            },
            {
                'nombre': 'DISTRIBUIDORA NORTE LTDA.',
                'cuit': '30-11223344-5',
                'domicilio': 'Mitre 456, San Isidro',
                'clave_fiscal': 'fiscal999',
                'clave_sec': 'sec123',
                'ptovta': '0001',
                'activo': True
            },
            {
                'nombre': 'TECNOLOGÍA Y DESARROLLO S.A.S.',
                'cuit': '30-55667788-9',
                'domicilio': 'Av. Santa Fe 2100, CABA',
                'clave_fiscal': 'tech2024',
                'clave_ciudad': 'ciudad456',
                'nombase': 'tech_db',
                'activo': True
            }
        ]
        
        created_count = 0
        
        for cliente_data in clientes_prueba:
            cliente, created = Cliente.objects.get_or_create(
                cuit=cliente_data['cuit'],
                defaults=cliente_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Cliente creado: {cliente.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Cliente ya existe: {cliente.nombre}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nProceso completado. {created_count} clientes nuevos creados.')
        )
