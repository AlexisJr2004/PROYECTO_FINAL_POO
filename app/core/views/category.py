from django.urls import reverse_lazy
from app.core.forms.category import CategoryForm
from app.core.models import Category
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class CategoryListView(PermissionMixin,ListViewMixin, ListView):
    template_name = 'core/categories/list.html'
    model = Category
    context_object_name = 'categories'
    permission_required = 'view_category'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(description__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('core:category_create')
        return context

class CategoryCreateView(PermissionMixin,CreateViewMixin, CreateView):
    model = Category
    template_name = 'core/categories/form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('core:category_list')
    permission_required = 'add_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Categoría'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        category = self.object
        messages.success(self.request, f"Éxito al crear la categoría {category.description}.")
        return response
    
class CategoryUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = Category
    template_name = 'core/categories/form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('core:category_list')
    permission_required = 'change_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Categoría'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        category = self.object
        messages.success(self.request, f"Éxito al actualizar la categoría {category.description}.")
        return response
    
class CategoryDeleteView(PermissionMixin,DeleteViewMixin, DeleteView):
    model = Category
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:category_list')
    permission_required = 'delete_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Categoría'
        context['description'] = f"¿Desea Eliminar la Categoría: {self.object.description}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente la categoría {self.object.description}."
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
    
