from rest_framework import serializers
from personajes.models import caballo, vaquero, arma

class CaballoSerializer(serializers.ModelSerializer):
    nombre = serializers.CharField(
        required=True,
        style={'input_type': 'text', 'placeholder': 'Nombre del caballo'}
    )
    raza = serializers.CharField(
        required=True,
        style={'input_type': 'text', 'placeholder': 'Raza del caballo'}
    )
    color = serializers.CharField(
        required=True,
        style={'input_type': 'color', 'placeholder': 'Seleccione un color'}
    )
    velocidad = serializers.ChoiceField(
        choices=caballo.nivel,  # Reemplazar con las opciones reales de niveles
        required=True,
        style={'input_type': 'select'}
    )
    resistencia = serializers.ChoiceField(
        choices=caballo.nivel,  # Reemplazar con las opciones reales de niveles
        required=True,
        style={'input_type': 'select'}
    )
    vaquero = serializers.PrimaryKeyRelatedField(
        queryset=vaquero.objects.all(),
        required=False,
        allow_null=True,
        style={'input_type': 'select', 'placeholder': 'Seleccione un vaquero (opcional)'}
    )

    class Meta:
        model = caballo
        fields = ['id', 'nombre', 'raza', 'color', 'velocidad', 'resistencia', 'vaquero']



class ArmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = arma
        fields = ['id', 'nombre', 'cantidad_balas', 'tipo_bala', 'tipo_arma', 'cadencia', 'vaquero']
        extra_kwargs = {
            'vaquero': {'required': False, 'allow_null': True}
        }


class VaqueroSerializer(serializers.ModelSerializer):
    # Relación con caballos y armas
    caballos = CaballoSerializer(many=True, read_only=True)
    armas = ArmaSerializer(many=True, read_only=True)

    # Campos personalizados para inputs especiales
    nuevo_caballo_nombre = serializers.CharField(
        write_only=True, required=False,
        style={'input_type': 'text', 'placeholder': 'Nombre del caballo'}
    )
    nuevo_caballo_raza = serializers.CharField(
        write_only=True, required=False,
        style={'input_type': 'text', 'placeholder': 'Raza del caballo'}
    )
    nuevo_caballo_color = serializers.CharField(
        write_only=True, required=False,
        style={'input_type': 'color', 'placeholder': 'Seleccione un color'}
    )
    nuevo_caballo_velocidad = serializers.ChoiceField(
        choices=caballo.nivel, write_only=True, required=False,
        style={'input_type': 'select'}
    )
    nuevo_caballo_resistencia = serializers.ChoiceField(
        choices=caballo.nivel, write_only=True, required=False,
        style={'input_type': 'select'}
    )

    # Campos adicionales para nueva_arma
    nueva_arma_nombre = serializers.CharField(
        write_only=True, required=False,
        style={'input_type': 'text', 'placeholder': 'Nombre del arma'}
    )
    nueva_arma_cantidad_balas = serializers.IntegerField(
        write_only=True, required=False, min_value=1,
        style={'input_type': 'number', 'placeholder': 'Cantidad de balas'}
    )
    nueva_arma_tipo_bala = serializers.ChoiceField(
        choices=arma.TipoBala, write_only=True, required=False,
        style={'input_type': 'select', 'placeholder': 'Tipo de bala'}
    )
    nueva_arma_tipo_arma = serializers.ChoiceField(
        choices=arma.TipoArma, write_only=True, required=False,
        style={'input_type': 'select', 'placeholder': 'Tipo de arma'}
    )
    nueva_arma_cadencia = serializers.ChoiceField(
        choices=arma.TipoCadencia, write_only=True, required=False,
        style={'input_type': 'select', 'placeholder': 'Cadencia del arma'}
    )

    class Meta:
        model = vaquero
        fields = [
            'id', 'nombre', 'apellido', 'edad', 'buscado', 'sexo',
            'caballos', 'armas',
            'nuevo_caballo_nombre', 'nuevo_caballo_raza', 'nuevo_caballo_color', 
            'nuevo_caballo_velocidad', 'nuevo_caballo_resistencia',
            'nueva_arma_nombre', 'nueva_arma_cantidad_balas',
            'nueva_arma_tipo_bala', 'nueva_arma_tipo_arma', 'nueva_arma_cadencia'
        ]

    def create(self, validated_data):
        # Procesamiento de datos adicionales para caballos y armas
        nuevo_caballo_nombre = validated_data.pop('nuevo_caballo_nombre', None)
        nuevo_caballo_raza = validated_data.pop('nuevo_caballo_raza', None)
        nuevo_caballo_color = validated_data.pop('nuevo_caballo_color', None)
        nuevo_caballo_velocidad = validated_data.pop('nuevo_caballo_velocidad', None)
        nuevo_caballo_resistencia = validated_data.pop('nuevo_caballo_resistencia', None)

        nueva_arma_nombre = validated_data.pop('nueva_arma_nombre', None)
        nueva_arma_cantidad_balas = validated_data.pop('nueva_arma_cantidad_balas', None)
        nueva_arma_tipo_bala = validated_data.pop('nueva_arma_tipo_bala', None)
        nueva_arma_tipo_arma = validated_data.pop('nueva_arma_tipo_arma', None)
        nueva_arma_cadencia = validated_data.pop('nueva_arma_cadencia', None)

        # Crear el vaquero
        vaquero_instance = vaquero.objects.create(**validated_data)

        # Crear el caballo relacionado, si los datos están presentes
        if nuevo_caballo_nombre and nuevo_caballo_raza:
            caballo.objects.create(
                nombre=nuevo_caballo_nombre,
                raza=nuevo_caballo_raza,
                color=nuevo_caballo_color,
                velocidad=nuevo_caballo_velocidad,
                resistencia=nuevo_caballo_resistencia,
                vaquero=vaquero_instance
            )

        # Crear el arma relacionada, si los datos están presentes
        if nueva_arma_nombre and nueva_arma_cantidad_balas:
            arma.objects.create(
                nombre=nueva_arma_nombre,
                cantidad_balas=nueva_arma_cantidad_balas,
                tipo_bala=nueva_arma_tipo_bala,
                tipo_arma=nueva_arma_tipo_arma,
                cadencia=nueva_arma_cadencia,
                vaquero=vaquero_instance
            )

        return vaquero_instance

    def validate(self, data):
        # Validar los campos relacionados con el nuevo caballo
        nuevo_caballo_nombre = data.get('nuevo_caballo_nombre')
        nuevo_caballo_raza = data.get('nuevo_caballo_raza')
        nuevo_caballo_color = data.get('nuevo_caballo_color')
        nuevo_caballo_velocidad = data.get('nuevo_caballo_velocidad')
        nuevo_caballo_resistencia = data.get('nuevo_caballo_resistencia')

        if any([nuevo_caballo_nombre, nuevo_caballo_raza, nuevo_caballo_color, 
                nuevo_caballo_velocidad, nuevo_caballo_resistencia]):
            required_caballo_fields = [
                ('nuevo_caballo_nombre', nuevo_caballo_nombre),
                ('nuevo_caballo_raza', nuevo_caballo_raza),
                ('nuevo_caballo_color', nuevo_caballo_color),
                ('nuevo_caballo_velocidad', nuevo_caballo_velocidad),
                ('nuevo_caballo_resistencia', nuevo_caballo_resistencia),
            ]
            for field_name, value in required_caballo_fields:
                if not value:
                    raise serializers.ValidationError({field_name: 'Este campo es requerido si estás creando un nuevo caballo.'})

        # Validar los campos relacionados con el nuevo arma
        nueva_arma_nombre = data.get('nueva_arma_nombre')
        nueva_arma_cantidad_balas = data.get('nueva_arma_cantidad_balas')
        nueva_arma_tipo_bala = data.get('nueva_arma_tipo_bala')
        nueva_arma_tipo_arma = data.get('nueva_arma_tipo_arma')
        nueva_arma_cadencia = data.get('nueva_arma_cadencia')

        if any([nueva_arma_nombre, nueva_arma_cantidad_balas, nueva_arma_tipo_bala, nueva_arma_tipo_arma, nueva_arma_cadencia]):
            required_arma_fields = [
                ('nueva_arma_nombre', nueva_arma_nombre),
                ('nueva_arma_cantidad_balas', nueva_arma_cantidad_balas),
                ('nueva_arma_tipo_bala', nueva_arma_tipo_bala),
                ('nueva_arma_tipo_arma', nueva_arma_tipo_arma),
                ('nueva_arma_cadencia', nueva_arma_cadencia),
            ]
            for field_name, value in required_arma_fields:
                if not value:
                    raise serializers.ValidationError({field_name: 'Este campo es requerido si estás creando un arma.'})

        return data



