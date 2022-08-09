# from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls.base import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# importando el decorador que hará lo mismo que un mixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from .models import Page
from .forms import PageForm

class StaffRequiredMixin(object):
    """Este mixin requerirá que el usuario sea miembro del staff"""
    # dispatch para que se configure el mixin:
    # si se trabajará con el decorador: staff_member_required usar:
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        # si el usuario no es staff y quiere crear, editar o eliminar alguna página, el sistema lo redireccionará al login:
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
        # la ventaja de usar el decorador es que por ejemplo si no estás logueado y quieres editar una página, serás direccionado al login de usuario y después de loguearte, el sistema te regresa a la vista de edición, algo que no se puede realizar con el otro método (sin decorador)

    # si no se trabaja con el decorador, usar:
    # def dispatch(self, request, *args, **kwargs):
        # si el usuario no es staff y quiere crear, editar o eliminar alguna página, el sistema lo redireccionará al login
        # if not request.user.is_staff:
            # return redirect(reverse_lazy('admin:login'))
        # return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)


# Create your views here.
# Vistas basadas en funciones
# devolver una lista de las instancias de un modelo
# def pages(request):
#     pages = get_list_or_404(Page)
#     return render(request, 'pages/pages.html', {'pages':pages})

# # devolver una instancia del modelo
# def page(request, page_id, page_slug):
#     page = get_object_or_404(Page, id=page_id)
#     return render(request, 'pages/page.html', {'page':page})


# Vistas basadas en clases:
class PageListView(ListView):
    model = Page


class PageDetailView(DetailView):
    model = Page


# Para vista para la creación de una página:
# sin decorador @method_decorator(staff_member_required)
# class PageCreate(StaffRequiredMixin, CreateView):
# con el decorador:
@method_decorator(staff_member_required, name='dispatch')
class PageCreate(CreateView):
    model = Page
    # importando para editar los formularios:
    form_class = PageForm # PageForm ya tiene incluido los fields que han sido comentado abajo
    # fields = ['title', 'content', 'order']

    # en caso registre correctamente la nueva página:
    # def get_success_url(self):
        # return reverse('pages:pages')

    # en caso registre correctamente la nueva página (más corto):
    success_url = reverse_lazy('pages:pages')



# Para editar una página:
# sin decorador @method_decorator(staff_member_required)
# class PageUpdate(StaffRequiredMixin, UpdateView):
# con el decorador:
@method_decorator(staff_member_required, name='dispatch')
class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm # PageForm ya tiene incluido los fields que han sido comentado abajo
    # fields = ['title', 'content', 'order']
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'


# Para eliminar una página:
# sin decorador @method_decorator(staff_member_required)
# class PageDelete(StaffRequiredMixin, DeleteView):
# con el decorador:
@method_decorator(staff_member_required, name='dispatch')
class PageDelete(DeleteView):
    model = Page
    success_url = reverse_lazy('pages:pages')