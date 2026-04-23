from django import forms
from .models import Clientes
import re
from django.core.exceptions import ValidationError

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['codigo', 'nombre', 'apellidopaterno', 'apellidomaterno', 'correo', 'telefono']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            # Validar formato de teléfono mexicano
            patron = re.compile(r'^\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}$')
            if not patron.match(telefono):
                raise ValidationError('Formato inválido. Use: (656) 123-4567 o 6561234567')
        return telefono
    
    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        instance = self.instance
        
        # Verificar si el correo ya existe (excepto el actual en edición)
        if Clientes.objects.filter(correo=correo).exclude(codigo=instance.codigo if instance.codigo else None).exists():
            raise ValidationError('Este correo ya está registrado')
        
        return correo


