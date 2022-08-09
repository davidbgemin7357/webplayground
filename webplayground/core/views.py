from django.shortcuts import render
from django.views.generic.base import TemplateView

# def home(request):
#     return render(request, "core/home.html")

# def sample(request):
#     return render(request, "core/sample.html")

class HomePageView(TemplateView):
    template_name = 'core/home.html'

    # sobreescritura del diccionario de contexto (normal):
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Mi super Web Playground'
    #     return context
    
    # como solo vamos a pasar un título, se puede reducir la sobreescritura del diccionario de contexto:
    def get(self, request, **kwargs):
        return render(request, self.template_name, {'title':'Mi Super Web Playground'})


class SamplePageView(TemplateView):
    template_name = 'core/sample.html'