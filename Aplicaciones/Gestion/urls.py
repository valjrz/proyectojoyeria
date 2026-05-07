from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('productos/', views.gestionproductos),
    path('registrarProducto/', views.registrarProducto),
    path('agregarProducto/', views.vistaAgregarProducto,name='agregar_producto'),
    path('edicionProducto/<codigo>', views.edicionProducto),
    path('editarProducto/',views.editarProducto),
    path('eliminacionProducto/<codigo>',views.eliminacionProducto ),

    path('categorias/', views.gestionCategorias),
    path('registrarCategoria/', views.registrarCategoria),
    path('agregarCategoria/', views.vistaAgregarCategoria, name='agregar_categoria'),
    path('eliminarCategoria/<codigo>', views.eliminacionCategoria),
    path('edicionCategoria/<codigo>', views.edicionCategoria),
    path('categoria/<str:codigo>/', views.productos_por_categoria, name='productos_por_categoria'),


    path('clientes/',views.gestionClientes, name='gestion_clientes'),
    path('agregarCliente/', views.vistaAgregarCliente, name='agregar_cliente'),
    path('edicionCliente/<codigo>', views.edicionCliente),
    path('eliminarCliente/<codigo>',views.eliminacionCliente),

    path('pedidos/', views.gestionPedidos ,name='gestion_pedidos'),
    path('agregarPedido/', views.vistaAgregarPedido, name='agregar_pedido'),
    path('edicionPedido/<str:codigo>', views.edicionPedido, name='editar_pedido'),
    path('eliminacionPedidos/<str:codigo>', views.eliminacionPedido, name='eliminar_pedido'),
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home_ecommerce'), name='logout'),
    path('', views.home_ecommerce, name='home_ecommerce'),

    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<codigo>', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/pagar', views.pagar_carrito, name='pagar_carrito'),
    path('carrito/eliminar/<codigo>', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('carrito/modificar/<str:codigo>/<str:accion>/', views.modificar_cantidad_carrito, name='modificar_cantidad_carrito'), 

    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),

]