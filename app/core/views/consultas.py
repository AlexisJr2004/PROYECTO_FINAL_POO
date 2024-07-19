from django.db.models import Count, Sum, Max
import plotly.graph_objs as go
from django.views.generic import TemplateView
from app.core.models import Company, Brand, Supplier, Line, Category, Product, Customer, PaymentMethod, Iva
from app.sales.models import Invoice, InvoiceDetail
from app.purchases.models import Purchase, PurchaseDetail
from app.security.models import User
from django.db.models import Q
from proy_sales.utils import generar_color_aleatorio_2
import json 
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from plotly.subplots import make_subplots

from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import plotly.figure_factory as ff
import plotly.colors as plc

class ConsultasTemplateView(TemplateView):
    template_name = 'components/consultas.html'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title1"]= "IC - Consultas"
        context["title2"]= "Datos sobre nuestro Sistema"
        context["title3"]= "Gráficos y Estadísticas"
        
        companies = Company.objects.all()
        brands = Brand.objects.filter(active=True)
        lines = Line.objects.filter(active=True)
        customers = Customer.objects.all()
        categories = Category.objects.filter(active=True)
        products = Product.objects.filter(active=True)
        payment_methods = PaymentMethod.objects.filter(active=True)
        users_admin = User.objects.filter(Q(is_superuser=True) & Q(is_staff=True) & Q(is_active=True))
        suppliers = Supplier.objects.filter(active=True)
        
        context['companies'] = companies
        context['total_companies'] = companies.count()
        
        context['brands'] = brands
        context['total_brands'] = brands.count()
        
        context['lines'] = lines
        context['total_lines'] = lines.count()
        
        context['suppliers'] = suppliers
        context['total_suppliers'] = suppliers.count()
        
        context['customers'] = customers
        context['total_customers'] = customers.count()
        
        context['categories'] = categories
        context['total_categories'] = categories.count()
        
        context['products'] = products
        context['total_products'] = products.count()
        
        context['payment_methods'] = payment_methods
        context['total_payment_methods'] = payment_methods.count()
        
        context['users_admin'] = users_admin
        context['total_users_admin'] = users_admin.count()
        
        # -------------------- > INVENTARIO
        # -------------------- > Productos por Categoría
        category_products = Category.objects.annotate(product_count=Count('products_categories')).filter(active=True)
        categories = [category.description for category in category_products]
        colors = generar_color_aleatorio_2(categories)
        product_counts = [category.product_count for category in category_products]
        
        trace = go.Bar(
            x=categories,
            y=product_counts,
            marker=dict(color=colors),
        )
        
        layout = go.Layout(
            title='Productos por Categoría',
            xaxis=dict(title='Categorías'),
            yaxis=dict(title='Número de Productos')
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        
        graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['graphJSON'] = graphJSON
        
        # -------------------- > Marcas con más productos
        brand_products = Brand.objects.annotate(product_count=Count('product_brands')).filter(active=True).order_by('-product_count')[:10]  # Top 10 marcas
        brands = [brand.description for brand in brand_products]
        colors = generar_color_aleatorio_2(brands)
        product_counts = [brand.product_count for brand in brand_products]
        
        trace_brands = go.Bar(
            x=brands,
            y=product_counts,
            marker=dict(color=colors),
        )
        
        layout_brands = go.Layout(
            title='Top 10 Marcas con Más Productos',
            xaxis=dict(title='Marcas'),
            yaxis=dict(title='Número de Productos')
        )
        
        fig_brands = go.Figure(data=[trace_brands], layout=layout_brands)
        
        brandGraphJSON = json.dumps(fig_brands, cls=PlotlyJSONEncoder)
        context['brandGraphJSON'] = brandGraphJSON
        
        # -------------------- > Productos por linea
        lines = Line.objects.all()
        line_labels = [line.description for line in lines]
        colors = generar_color_aleatorio_2(line_labels)
        product_counts = [Product.objects.filter(line=line).count() for line in lines]
        
        trace_lines = go.Pie(
            labels=line_labels,
            values=product_counts,
            marker=dict(colors=colors),
        )
        
        layout_lines = go.Layout(
            title='Distribución de Productos por Línea'
        )
        
        fig_lines = go.Figure(data=[trace_lines], layout=layout_lines)

        lineGraphJSON = json.dumps(fig_lines, cls=PlotlyJSONEncoder)
        context['lineGraphJSON'] = lineGraphJSON
        
        # -------------------- > Tipo de contribuyentes 
        special_count = Company.objects.filter(taxpayer_type='special').count()
        ordinary_count = Company.objects.filter(taxpayer_type='ordinary').count()

        labels = ['Contribuyente Especial', 'Contribuyente Ordinario']
        values = [special_count, ordinary_count]

        trace_c = go.Pie(labels=labels, values=values)

        layout_c = go.Layout(
            title='Empresas por Tipo de Contribuyente'
        )

        fig_c = go.Figure(data=[trace_c], layout=layout_c)
        
        cJSON = json.dumps(fig_c, cls=PlotlyJSONEncoder)
        context['cJSON'] = cJSON
        
        # -------------------- > Clientes por género
        male_count = Customer.objects.filter(gender='M').count()
        female_count = Customer.objects.filter(gender='F').count()
        other_count = Customer.objects.filter(gender='O').count()

        labels = ['Masculino', 'Femenino', 'Otro']
        colors = ['#1f77b4', '#ff0080 ', '#5b5b5b'] 
        values = [male_count, female_count, other_count]

        trace_gender = go.Pie(labels=labels, values=values, marker=dict(colors=colors))

        layout_gender = go.Layout(
            title='Distribución de Clientes por Género'
        )

        fig_gender = go.Figure(data=[trace_gender], layout=layout_gender)
        
        genderGraphJSON = json.dumps(fig_gender, cls=PlotlyJSONEncoder)
        context['genderGraphJSON'] = genderGraphJSON
        
        # -------------------- > Productos con mas stock
        products = Product.objects.order_by('-stock')[:10]
        product_names = [product.description for product in products]
        colors = generar_color_aleatorio_2(product_names)
        stock_values = [product.stock for product in products]

        trace_stock = go.Bar(
            x=stock_values,
            y=product_names,
            orientation='h',
            marker=dict(color=colors),
        )

        layout_stock = go.Layout(
            title='Productos con Más Stock',
            xaxis=dict(title='Cantidad en Stock'),
            yaxis=dict(title='Producto', automargin=True),
            margin=dict(l=150),  # Ajuste para etiquetas largas
        )

        fig_stock = go.Figure(data=[trace_stock], layout=layout_stock)
        stockGraphJSON = json.dumps(fig_stock, cls=PlotlyJSONEncoder)
        context['stockGraphJSON'] = stockGraphJSON
        
        # -------------------- > Productos con IVA mas alto
        top_ivas = Iva.objects.annotate(num_products=Count('product_iva')).order_by('-num_products')[:5]
        iva_descriptions = [iva.description for iva in top_ivas]
        colors = generar_color_aleatorio_2(iva_descriptions)
        num_products = [iva.num_products for iva in top_ivas]

        trace_iva = go.Bar(
            x=num_products,
            y=iva_descriptions,
            orientation='h',
            marker=dict(color=colors),
        )

        layout_iva = go.Layout(
            title='Productos con IVA Más Utilizado',
            xaxis=dict(title='Número de Productos'),
            yaxis=dict(title='IVA', automargin=True),
            margin=dict(l=150),  # Ajuste para etiquetas largas
        )

        fig_iva = go.Figure(data=[trace_iva], layout=layout_iva)
        IvaGraphJSON = json.dumps(fig_iva, cls=PlotlyJSONEncoder)
        context['IvaGraphJSON'] = IvaGraphJSON
        
        # -------------------- > VENTAS
        # Obtener ventas diarias y cantidad de productos vendidos
        daily_sales = (
            Invoice.objects.filter(active=True)
            .annotate(date=TruncDate('issue_date'))
            .values('date')
            .annotate(
                total_sales=Sum('total'),
                products_sold=Sum('detail__quantity')
            )
            .order_by('date')
        )

        # Convertir los datos a listas para Plotly
        dates = [sale['date'].strftime('%Y-%m-%d') for sale in daily_sales]
        total_sales = [float(sale['total_sales']) for sale in daily_sales]
        products_sold = [int(sale['products_sold']) for sale in daily_sales]

        # Calcular la dirección de las flechas
        directions = []
        for i in range(len(total_sales)):
            if i == 0:
                directions.append('triangle-up')
            else:
                if total_sales[i] > total_sales[i-1]:
                    directions.append('triangle-up')
                elif total_sales[i] < total_sales[i-1]:
                    directions.append('triangle-down')
                else:
                    directions.append('circle')

        trace = go.Scatter(
            x=dates, 
            y=total_sales, 
            mode='lines+markers',
            name='Ventas Diarias',
            line=dict(color='#17BECF'),
            marker=dict(
                size=10,
                symbol=directions,
                color='#17BECF',
                line=dict(width=2, color='DarkSlateGrey')
            ),
            text=products_sold,  # Añadimos la cantidad de productos vendidos como texto
            customdata=products_sold  # Añadimos la cantidad de productos vendidos como datos personalizados
        )

        layout = go.Layout(
            title='Escala de Ventas',
            xaxis=dict(title='Fecha', tickangle=45, tickformat='%Y-%m-%d'),
            yaxis=dict(title='Total Ventas'),
            hovermode='x unified'
        )

        fig = go.Figure(data=[trace], layout=layout)

        # Añadir rangeslider y botones de selección de rango
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1 semana", step="day", stepmode="backward"),
                    dict(count=1, label="1 mes", step="month", stepmode="backward"),
                    dict(count=6, label="6 meses", step="month", stepmode="backward"),
                    dict(count=1, label="1 año", step="year", stepmode="backward"),
                    dict(step="all", label="Todo")
                ])
            )
        )

        # Configurar el hover para mostrar la fecha, el total de ventas, la tendencia y la cantidad de productos vendidos
        fig.update_traces(
            hovertemplate='Fecha: %{x}<br>Ganancias de Ventas: $%{y:.2f}<br>Productos Vendidos: %{customdata}<br>'
        )

        # Convertir gráfico a JSON para pasarlo al contexto
        salesGraphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['salesGraphJSON'] = salesGraphJSON

        # -------------------- > Productos mas vendidos
        top_products = (
            InvoiceDetail.objects.values('product__description')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')[:10]
        )

        product_names = [product['product__description'] for product in top_products]
        total_quantities = [product['total_quantity'] for product in top_products]
        colors = generar_color_aleatorio_2(product_names)

        # Crear el gráfico de barras horizontales
        trace = go.Bar(
            x=total_quantities,
            y=product_names,
            orientation='h',
            marker=dict(color=colors),
            name='Productos más Vendidos'
        )

        layout = go.Layout(
            title='Top 10 Productos más Vendidos',
            xaxis=dict(title='Cantidad Vendida'),
            yaxis=dict(title='Producto'),
            margin=dict(l=150)
        )

        fig = go.Figure(data=[trace], layout=layout)

        # Convertir gráfico a JSON para pasarlo al contexto
        topProductsGraphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['topProductsGraphJSON'] = topProductsGraphJSON
        
        # -------------------- > Metodos de pago mas utilizados
        payment_methods_sales = (
            Invoice.objects.filter(active=True)
            .values('payment_method__description')
            .annotate(total_sales=Sum('total'))
            .order_by('-total_sales')
        )
        
        labels = [sale['payment_method__description'] for sale in payment_methods_sales]
        values = [float(sale['total_sales']) for sale in payment_methods_sales]
        colors = generar_color_aleatorio_2(labels)
        trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors))

        layout = go.Layout(
            title='Proporción de Ventas por Método de Pago'
        )

        fig = go.Figure(data=[trace], layout=layout, )

        # Convertir gráfico a JSON para pasarlo al contexto
        paymentMethodsGraphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['paymentMethodsGraphJSON'] = paymentMethodsGraphJSON
        
        # -------------------- > Facturas por estado
        invoice_status_counts = (
            Invoice.objects.values('state')
            .annotate(count=Count('id'))
            .order_by('state')
        )
        labels = ['Factura', 'Anulada', 'Modificada']
        values = [0, 0, 0]
        colors = ['#87CEFA', '#F08080', '#90EE90'] 

        for item in invoice_status_counts:
            if item['state'] == 'F':
                values[0] = item['count']
            elif item['state'] == 'A':
                values[1] = item['count']
            elif item['state'] == 'M':
                values[2] = item['count']

        trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors))

        layout = go.Layout(
            title='Estado de Facturas'
        )

        fig = go.Figure(data=[trace], layout=layout)

        invoiceStatusGraphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['invoiceStatusGraphJSON'] = invoiceStatusGraphJSON
        
        # -------------------- > Clientes con mas compras
        top_customers = (
            Invoice.objects.filter(active=True)
            .values('customer__first_name', 'customer__last_name')
            .annotate(total_sales=Sum('total'))
            .order_by('-total_sales')[:10]
        )
        
        customer_names = [f"{customer['customer__first_name']} {customer['customer__last_name']}" for customer in top_customers]
        total_sales = [float(customer['total_sales']) for customer in top_customers]
        colors = generar_color_aleatorio_2(customer_names)
        
        trace = go.Bar(
            x=customer_names,
            y=total_sales,
            marker=dict(color=colors),
        )
        
        layout = go.Layout(
            title='Top 10 Clientes con Más Compras',
            xaxis=dict(title='Cliente'),
            yaxis=dict(title='Total Compras')
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        
        topCustomersGraphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['topCustomersGraphJSON'] = topCustomersGraphJSON
        
        # -------------------- > Compras
        # -------------------- > Compras por proveedor
        purchases = Purchase.objects.filter(active=True).order_by('issue_date')

        # Crear listas para almacenar los datos del gráfico
        suppliers = []
        start_dates = []
        end_dates = []
        durations = []

        # Recorrer cada compra para obtener los datos
        for purchase in purchases:
            suppliers.append(purchase.supplier.name)  # Nombre del proveedor
            start_dates.append(purchase.issue_date.strftime('%Y-%m-%d'))  # Fecha de emisión
            end_dates.append(purchase.issue_date.strftime('%Y-%m-%d'))  # Misma fecha como fin (solo para ejemplo)
            durations.append(1)  # Duración arbitraria de 1 día para cada compra (solo para ejemplo)

        # Crear el objeto de figura para el gráfico de Gantt
        fig = go.Figure()

        # Añadir trazos de Gantt para cada compra
        for i in range(len(purchases)):
            fig.add_trace(go.Bar(
                x=[suppliers[i], suppliers[i]],
                y=[start_dates[i], end_dates[i]],
                orientation='h',
                name=f'Compra {i+1}',
                marker=dict(
                    color='rgba(58, 71, 80, 0.6)',
                    line=dict(color='rgba(58, 71, 80, 1.0)', width=1)
                ),
                width=durations[i],
                hoverinfo='text',
                text=f'Fecha de emisión: {start_dates[i]}<br>Proveedor: {suppliers[i]}'
            ))

        # Configuración del diseño del gráfico
        fig.update_layout(
            title='Diagrama de Gantt de Compras por Proveedor',
            xaxis=dict(
                title='Proveedor',
                showgrid=True,
                zeroline=True
            ),
            yaxis=dict(
                title='Fechas',
                showgrid=True,
                zeroline=True
            ),
            barmode='stack',
            hovermode='closest',
            showlegend=True
        )
        
        topPurchasesSalesGraphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        context['topPurchasesSalesGraphJSON'] = topPurchasesSalesGraphJSON
        
        # -------------------- > Productos comprados
        daily_purchases = (
            Purchase.objects.filter(active=True)
            .annotate(date=TruncDate('issue_date'))
            .values('date')
            .annotate(total_purchases=Sum('total'))
            .order_by('date')
        )

        # Convertir los datos a listas para Plotly
        dates = [purchase['date'].strftime('%Y-%m-%d') for purchase in daily_purchases]
        total_purchases = [float(purchase['total_purchases']) for purchase in daily_purchases]

        # Calcular la dirección de las flechas
        directions = []
        for i in range(len(total_purchases)):
            if i == 0:
                directions.append('triangle-up')
            else:
                if total_purchases[i] > total_purchases[i-1]:
                    directions.append('triangle-up')
                elif total_purchases[i] < total_purchases[i-1]:
                    directions.append('triangle-down')
                else:
                    directions.append('circle')

        # Crear el trazo del gráfico de líneas y marcadores
        trace = go.Scatter(
            x=dates,
            y=total_purchases,
            mode='lines+markers',
            name='Compras Diarias',
            line=dict(color='#17BECF'),
            marker=dict(
                size=10,
                symbol=directions,
                color='#17BECF',
                line=dict(width=2, color='DarkSlateGrey')
            ),
            customdata=total_purchases  # Datos personalizados (opcional)
        )

        # Diseño del gráfico
        layout = go.Layout(
            title='Escala de Compras',
            xaxis=dict(title='Fecha', tickangle=45, tickformat='%Y-%m-%d'),
            yaxis=dict(title='Total Compras'),
            hovermode='x unified'
        )

        # Crear la figura
        fig = go.Figure(data=[trace], layout=layout)

        # Añadir rangeslider y botones de selección de rango
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="1 semana", step="day", stepmode="backward"),
                    dict(count=1, label="1 mes", step="month", stepmode="backward"),
                    dict(count=6, label="6 meses", step="month", stepmode="backward"),
                    dict(count=1, label="1 año", step="year", stepmode="backward"),
                    dict(step="all", label="Todo")
                ])
            )
        )

        # Configurar el hover para mostrar la fecha, el total de compras y la tendencia
        fig.update_traces(
            hovertemplate='Fecha: %{x}<br>Total Compras: $%{y:.2f}<br>'
        )

        # Convertir gráfico a JSON para pasarlo al contexto
        purchasesGraphJSON = fig.to_json()
        context['purchasesGraphJSON'] = purchasesGraphJSON
        
        # -------------------- > Productos mas comprados
        top_products = (
            InvoiceDetail.objects.filter(invoice__active=True)
            .values('product__description')
            .annotate(total_quantity=Sum('quantity'))
            .order_by('-total_quantity')
        )

        # Convertir los datos a listas para Plotly
        product_names = [product['product__description'] for product in top_products]
        quantities = [product['total_quantity'] for product in top_products]
        colors = generar_color_aleatorio_2(product_names)
        
        # Calcular el porcentaje acumulado
        total_quantity = sum(quantities)
        cumulative_percentages = [sum(quantities[:i + 1]) / total_quantity * 100 for i in range(len(quantities))]
        
        # Crear el trazo de barras para las cantidades y la línea para el porcentaje acumulado
        trace_bars = go.Bar(
            x=product_names,
            y=quantities,
            name='Cantidad',
            marker=dict(color=colors)
        )

        trace_line = go.Scatter(
            x=product_names,
            y=cumulative_percentages,
            name='Porcentaje Acumulado',
            yaxis='y2',
            mode='lines+markers',
            marker=dict(color='red')
        )

        # Diseño del gráfico
        layout = go.Layout(
            title='Diagrama de Pareto - Productos más Comprados',
            xaxis=dict(title='Productos'),
            yaxis=dict(title='Cantidad'),
            yaxis2=dict(title='Porcentaje Acumulado', overlaying='y', side='right', range=[0, 100]),
            legend=dict(x=0.7, y=1.1, orientation='h')
        )

        # Crear la figura con los trazos y el diseño
        fig = go.Figure(data=[trace_bars, trace_line], layout=layout)

        # Convertir gráfico a JSON para pasarlo al contexto
        paretoGraphJSON = fig.to_json()
        context['paretoGraphJSON'] = paretoGraphJSON
        
        # -------------------- > Mapas de Usuarios 
        # -------------------- > Mapa de Proveedores
        suppliers = Supplier.objects.filter(active=True)
        # Crear listas para almacenar los datos del mapa
        names = []
        latitudes = []
        longitudes = []
        # Recorrer cada proveedor para obtener los datos
        for supplier in suppliers:
            names.append(supplier.name)
            latitudes.append(float(supplier.latitude))
            longitudes.append(float(supplier.longitude))

        # Crear el objeto de figura para el mapa
        fig = go.Figure()

        # Agregar los marcadores de proveedores
        fig.add_trace(go.Scattergeo(
            lon=longitudes,
            lat=latitudes,
            text=names,
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.8,
                symbol='circle',
                line=dict(
                    width=1,
                    color="#17FF00"
                ),
                color="#17FF00",
                colorbar_title="Proveedores"
            )
        ))

        # Configuración del diseño del mapa con capas de color adicionales
        fig.update_layout(
            title='Mapa Global de Proveedores',
            geo=dict(
                scope='world',
                projection_type='natural earth',
                showland=True,
                landcolor="#3A3A3A",  # Color de la tierra
                subunitcolor="#C6C6C6",  # Color de las subunidades (como estados o provincias)
                countrycolor="#C6C6C6",  # Color de los bordes de los países
                countrywidth=1,
                subunitwidth=0.5,
                showcountries=True,
                showcoastlines=True,
                coastlinecolor="#1F1F1F",  # Color de las costas
                showocean=True,
                oceancolor="#CBCBCB",  # Color de los océanos
            ),
            height=600,
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )

        # Convertir la figura a JSON utilizando PlotlyJSONEncoder
        supplierMapJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        # Pasar el JSON del mapa al contexto
        context['supplierMapJSON'] = supplierMapJSON
        
        # -------------------- > Mapa de Clientes
        customers = Customer.objects.all()
        names = []
        latitudes = []
        longitudes = []
        # Recorrer cada proveedor para obtener los datos
        for customer in customers:
            names.append(customer.first_name + ' ' + customer.last_name)
            if customer.latitude:
                latitudes.append(float(customer.latitude))
            if customer.longitude:
                longitudes.append(float(customer.longitude))

        # Crear el objeto de figura para el mapa
        fig = go.Figure()

        # Agregar los marcadores de proveedores
        fig.add_trace(go.Scattergeo(
            lon=longitudes,
            lat=latitudes,
            text=names,
            mode='markers',
            marker=dict(
                size=8,
                opacity=0.8,
                symbol='circle',
                line=dict(
                    width=1,
                    color="#17FF00"
                ),
                color="#17FF00",
                colorbar_title="Clientes"
            )
        ))

        # Configuración del diseño del mapa con capas de color adicionales
        fig.update_layout(
            title='Mapa Global de Clientes',
            geo=dict(
                scope='world',
                projection_type='natural earth',
                showland=True,
                landcolor="#3A3A3A",  # Color de la tierra
                subunitcolor="#C6C6C6",  # Color de las subunidades (como estados o provincias)
                countrycolor="#C6C6C6",  # Color de los bordes de los países
                countrywidth=1,
                subunitwidth=0.5,
                showcountries=True,
                showcoastlines=True,
                coastlinecolor="#1F1F1F",  # Color de las costas
                showocean=True,
                oceancolor="#CBCBCB",  # Color de los océanos
            ),
            height=600,
            margin={"r": 0, "t": 40, "l": 0, "b": 0}
        )

        # Convertir la figura a JSON utilizando PlotlyJSONEncoder
        customerMapJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
        # Pasar el JSON del mapa al contexto
        context['customerMapJSON'] = customerMapJSON

        return context