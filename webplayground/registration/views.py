from os import name
from django.shortcuts import render

# sin email oblogatorio al registrarse:
from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms

# para hacer editable el perfil de usuario, se debe reemplazar TemplateView por UpdateView en la clase ProfileUpdate
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

# con email obligatorio al registrarse:
from .forms import UserCreationFormWithEmail, ProfileForm, EmailForm

# para crear el perfil de usuario, el usuario debe existir (sino no tendría sentido), por ello importar:
from django.contrib.auth.decorators import login_required

from .models import Profile

# Create your views here.
class SignUpView(CreateView):
    # sin email obligatorio al registrarse:
    # form_class = UserCreationForm
    # con el email obligatorio al registrarse
    form_class = UserCreationFormWithEmail
    # si no se usa el método get_success_url, usar:
    # success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    # el método get_success_url permite concatenar un '?register', lo cual puede ser usado para generar una retroalimentación en caso el usuario haya sido creado satisfactoriamente
    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        # nos devuelve el formulario
        form = super(SignUpView, self).get_form()
        # modificando en tiempo real (sobreescribiendo el widget):
        #           esto se obtiene al precionar F12 y verificar los campos del formulario
        form.fields['username'].widget = forms.TextInput(attrs={'class':'form-control mb-2', 'placeholder':'Nombre de usuario'})
        # agregamos el campo email que ha sido agregado:
        form.fields['email'].widget = forms.EmailInput(attrs={'class':'form-control mb-2', 'placeholder':'Dirección email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class':'form-control mb-2', 'placeholder':'Repite la constraseña'})

        return form


@method_decorator(login_required, name='dispatch')
# para hacer editable el perfil de usuario, reemplazar TemplateView por UpdateView
# class ProfileUpdate(TemplateView):
class ProfileUpdate(UpdateView):
    # UpdateView
    # model = Profile <-- comentamos porque estamos importando el ProfileForm (que ya tiene el model=Profile) de forms
    form_class = ProfileForm
    # UpdateView
    # los campos que queremos que muestre:
    # fields = ['avatar', 'bio', 'link'] <-- se comenta esto ya que el Profile form ya trae incluido los campos
    success_url = reverse_lazy('profile')

    # TemplateView
    template_name = 'registration/profile_form.html'

    # UpdateView
    def get_object(self):
        # recuperar el objeto que se va a editar
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile


@method_decorator(login_required, name='dispatch')
class EmailUpdate(UpdateView):
    form_class = EmailForm
    success_url = reverse_lazy('profile')
    template_name = 'registration/profile_email_form.html'

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super(EmailUpdate, self).get_form()
        # Modificar en tiempo real:
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class':'form-control mb-2', 'placeholder': 'Email'}
        )
        return form