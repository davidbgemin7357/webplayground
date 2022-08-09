from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields, widgets

from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Requerido, 254 caracteres como máximo y debe ser válido')

    class Meta:
        model = User
        # agregamos el campo email (que por defecto django no lo incorpora)
        fields = ('username', 'email', 'password1', 'password2')

    # * método para validar que el nuevo usuario a crear tiene un correo que aún no ha sido registrado en la bd
    # usar clean_campoAmodificar
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # si existe un usuario con un correo ya existente, invoca el error ValidationError
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya está registrado, prueba con otro.')
            
        return email

# para hacer que el formulario de perfil tenga los estilos de bootstrap
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'link']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control-file mt-3'}),
            'bio': forms.Textarea(attrs={'class':'form-control mt-3', 'row':3, 'placeholder':'Biografía'}),
            'link': forms.URLInput(attrs={'class':'form-control mt-3', 'placeholder':'Enlace'}),
        }


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # 1. el email debe haber cambiado
        if 'email' in self.changed_data:
            # 2. el email debe haber sido creado para que luego sea guardado
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('El email ya está registrado, prueba con otro.')
        return email