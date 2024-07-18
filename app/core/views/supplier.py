import json
from django.urls import reverse_lazy
from app.core.forms.supplier import SupplierForm
from app.core.models import Supplier
from app.security.instance.menu_module import MenuModule
from app.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q

class SupplierListView(PermissionMixin,ListViewMixin, ListView):
    template_name = 'core/suppliers/list.html'
    model = Supplier
    context_object_name = 'suppliers'
    permission_required = 'view_supplier'
    
    def get_queryset(self):
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(name__icontains=q1), Q.OR) 
            self.query.add(Q(ruc__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['permission_add'] = context['permissions'].get('add_supplier','')
        context['create_url'] = reverse_lazy('core:supplier_create')
        return context

class SupplierCreateView(PermissionMixin, CreateViewMixin, CreateView):
    model = Supplier
    template_name = 'core/suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'add_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Proveedor'
        context['back_url'] = self.success_url

        # Obtener todos los proveedores activos con coordenadas válidas
        suppliers = Supplier.objects.filter(
            Q(active=True) & 
            ~Q(latitude__isnull=True) & 
            ~Q(longitude__isnull=True)
        )
        
        # Convertir los proveedores a JSON para usar en JavaScript
        suppliers_data = [
            {
                'name': supplier.name,
                'latitude': float(supplier.latitude),
                'longitude': float(supplier.longitude)
            }
            for supplier in suppliers
        ]
        context['suppliers_json'] = json.dumps(suppliers_data)

        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        supplier = self.object
        messages.success(self.request, f"Éxito al crear al proveedor {supplier.name}.")
        return response
    
class SupplierUpdateView(PermissionMixin,UpdateViewMixin, UpdateView):
    model = Supplier
    template_name = 'core/suppliers/form.html'
    form_class = SupplierForm
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'change_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Proveedor'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        supplier = self.object
        messages.success(self.request, f"Éxito al actualizar el proveedor {supplier.name}.")
        return response
    
class SupplierDeleteView(PermissionMixin,DeleteViewMixin, DeleteView):
    model = Supplier
    template_name = 'core/delete.html'
    success_url = reverse_lazy('core:supplier_list')
    permission_required = 'delete_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Proveedorl'
        context['description'] = f"¿Desea Eliminar al Proveedor: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente al proveedor {self.object.name}."
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)