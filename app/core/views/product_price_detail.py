# from django.urls import reverse_lazy
# from app.core.forms.product_price_detail import ProductPriceDetailForm
# from app.core.models import Product, ProductPriceDetail
# from app.security.instance.menu_module import MenuModule
# from app.security.mixins.mixins import (
#     CreateViewMixin,
#     DeleteViewMixin,
#     ListViewMixin,
#     PermissionMixin,
#     UpdateViewMixin,
# )
# from django.views.generic import CreateView, ListView, UpdateView, DeleteView
# from django.contrib import messages
# from django.db.models import Q

# from app.core.models import Notification


# from django.http import JsonResponse
# from decimal import Decimal


# class ProductPriceDetailListView(PermissionMixin, ListViewMixin, ListView):
#     template_name = "core/product_price_details/list.html"
#     model = ProductPriceDetail
#     context_object_name = "product_price_details"
#     permission_required = "view_product_price_detail"

#     def get_queryset(self):
#         queryset = self.model.objects.select_related('product', 'productpreci').order_by("id")
#         q1 = self.request.GET.get("q")
#         if q1:
#             queryset = queryset.filter(
#                 Q(product__name__icontains=q1) |
#                 Q(productpreci__value__icontains=q1) |
#                 Q(observation__icontains=q1)
#             )
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["create_url"] = reverse_lazy("core:product_price_detail_create")
#         context["title1"] = "Detalles de Precios de Productos"
#         context["title2"] = "Listado de Detalles de Precios"
#         return context


# class ProductPriceDetailCreateView(PermissionMixin, CreateViewMixin, CreateView):
#     model = ProductPriceDetail
#     template_name = "core/product_price_details/form.html"
#     form_class = ProductPriceDetailForm
#     success_url = reverse_lazy("core:product_price_detail_list")
#     permission_required = "add_product_price_detail"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context["grabar"] = "Grabar Detalle de Precio de Producto"
#         context["back_url"] = self.success_url
#         return context

#     def post(self, request, *args, **kwargs):
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             line_id = request.POST.get('line')
#             category_id = request.POST.get('category')
#             product_id = request.POST.get('product')
#             type_increment = request.POST.get('type_increment')
#             value = Decimal(request.POST.get('value', 0))

#             products = Product.objects.filter(line_id=line_id)
#             if category_id:
#                 products = products.filter(category__id=category_id)
#             if product_id:
#                 products = products.filter(id=product_id)

#             results = []
#             for product in products:
#                 old_price = product.price
#                 if type_increment == 'P':  # Porcentaje
#                     increment = old_price * (value / Decimal('100'))
#                 else:  # Valor fijo
#                     increment = value

#                 results.append({
#                     'id': product.id,
#                     'name': product.name,
#                     'increment': str(round(increment, 2)),
#                     'old_price': str(old_price),
#                 })

#             return JsonResponse(results, safe=False)

#         return super().post(request, *args, **kwargs)

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         product_price_detail = self.object
#         success_message = f"Éxito al crear el detalle de precio de producto {product_price_detail.product}."
#         messages.success(self.request, success_message)
#         Notification.objects.create(message=success_message)
#         return response


# class ProductPriceDetailUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
#     model = ProductPriceDetail
#     template_name = "core/product_price_details/form.html"
#     form_class = ProductPriceDetailForm
#     success_url = reverse_lazy("core:product_price_detail_list")
#     permission_required = "change_product_price_detail"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context["grabar"] = "Actualizar Detalle de Precio de Producto"
#         context["back_url"] = self.success_url
#         return context

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         product_price_detail = self.object
#         success_message = f"Éxito al actualizar el detalle de precio de producto {product_price_detail.product}."
#         messages.success(self.request, success_message)
#         Notification.objects.create(message=success_message)
#         return response


# class ProductPriceDetailDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
#     model = ProductPriceDetail
#     template_name = "core/delete.html"
#     success_url = reverse_lazy("core:product_price_detail_list")
#     permission_required = "delete_product_price_detail"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data()
#         context["grabar"] = "Eliminar Detalle de Precio de Producto"
#         context["description"] = f"¿Desea Eliminar el Detalle de Precio de Producto?"
#         context["back_url"] = self.success_url
#         return context

#     def delete(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         success_message = f"Éxito al eliminar lógicamente el detalle de precio del producto {self.object.product}."
#         messages.success(self.request, success_message)
#         Notification.objects.create(message=success_message)
#         # Cambiar el estado de eliminado lógico
#         # self.object.deleted = True
#         # self.object.save()
#         return super().delete(request, *args, **kwargs)
