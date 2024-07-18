from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import PermissionMixin
from django.views.generic import TemplateView

class ModuloTemplateView(PermissionMixin, TemplateView):
    template_name = 'components/modulos.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"] = "IC - Modulos"
        context["title2"] = "Modulos Disponibles"
        
        # Llenar los módulos en el contexto
        MenuModule(self.request).fill(context)
        
        # Asegúrate de que 'modules' esté en el contexto y ordena alfabéticamente
        if 'modules' in context:
            context['modules'] = sorted(context['modules'], key=lambda module: module['name'])
        
        print(context)
        return context
