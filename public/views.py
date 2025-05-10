from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from products.models import Design, Tag

class HomePageViewPublic(TemplateView):
    template_name = 'public/pages/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_desings = Design.objects.count()
        context['all_desings'] = all_desings
        return context

class CatalogPageViewPublic(ListView):
    template_name = 'public/pages/catalog.html'
    model = Design
    context_object_name = 'playeras'
    paginate_by = 12  # Cambia este número según cuántos elementos quieras por página

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtro por búsqueda
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) |
                Q(name__icontains=query) |
                Q(tags__name__icontains=query) 
            ).distinct()

        # Filtro por etiquetas
        tags = self.request.GET.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__name__in=tags).distinct()

        return queryset.order_by('-name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()  # Todas las etiquetas disponibles
        context['selected_tags'] = self.request.GET.getlist('tags')  # Etiquetas seleccionadas
        return context

class AboutUsPageViewPublic(TemplateView):
    template_name = 'public/pages/about_us.html'

class QuestionPageViewPublic(TemplateView):
    template_name = 'public/pages/question.html'
def custom_404_view(request, exception):
    return render(request, 'public/errors/404.html', {}, status=404)

def custom_403_view(request, exception):
    return render(request, 'public/errors/403.html', {}, status=403)