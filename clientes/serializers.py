from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Cliente.
    """
    
    cuit_sin_guiones = serializers.ReadOnlyField()
    tiene_clave_fiscal = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def validate_cuit(self, value):
        """
        Validación personalizada para el CUIT.
        """
        if not value:
            raise serializers.ValidationError("El CUIT es requerido.")
        
        # Verificar formato básico
        if len(value) != 13 or value.count('-') != 2:
            raise serializers.ValidationError("El CUIT debe tener el formato XX-XXXXXXXX-X")
        
        return value


class ClienteListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listas de clientes.
    """
    
    class Meta:
        model = Cliente
        fields = [
            'id',
            'nombre',
            'cuit',
            'domicilio',
            'activo',
            'fecha_creacion'
        ]


class ClienteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para crear nuevos clientes.
    """
    
    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'cuit',
            'domicilio',
            'clave_fiscal',
            'clave_ciudad',
            'clave_arba',
            'activo'
        ]
    
    def validate_nombre(self, value):
        """
        Validación para el nombre del cliente.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre es requerido.")
        return value.strip()


class ClienteUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para actualizar clientes existentes.
    """
    
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']
    
    def validate_cuit(self, value):
        """
        Validación del CUIT en actualizaciones.
        """
        if value and self.instance and value != self.instance.cuit:
            # Verificar que el nuevo CUIT no esté en uso
            if Cliente.objects.filter(cuit=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Ya existe un cliente con este CUIT.")
        return value
