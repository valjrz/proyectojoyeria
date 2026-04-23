from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required, user_passes_test


from . models import Productos
from . models import Categoria
from . models import Clientes
from . forms import ClienteForm
from . models import Pedidos 
import random
from datetime import datetime
from django.contrib import messages 

# Create your views here.
# Función para verificar si el usuario es administrador
def es_admin(user):
    return user.is_staff

#vistas productos
@login_required
@user_passes_test(es_admin)
def gestionproductos(request): #request es una peticion modelo cliente servidor
    productos = Productos.objects.all() #listado de todos los productos 
    return render(request, "gestionproductos.html", {"productos":productos})

@login_required
@user_passes_test(es_admin)
def registrarProducto(request):
    codigo=request.POST['codigo']
    nombre=request.POST['nombre']
    categoria_id=request.POST['categoria']
    imagen = request.FILES.get('imagen', None)
    precio = request.POST['precio']

    categoria = get_object_or_404(Categoria, codigo=categoria_id)
    productos = Productos.objects.create(
        codigo=codigo, nombre=nombre, categoria=categoria, imagen=imagen, precio=precio)
    messages.success(request,'Producto Registrado!')
    return redirect('/')

@login_required
@user_passes_test(es_admin)
def vistaAgregarProducto(request):
    categorias = Categoria.objects.all()
    return render(request, "agregarProductos.html", {"categorias": categorias})

@login_required
@user_passes_test(es_admin)
def edicionProducto(request,codigo):
    productos = get_object_or_404(Productos, codigo=codigo)
    return render(request, "edicionProducto.html", {"productos":productos})

@login_required
@user_passes_test(es_admin)
def editarProducto(request):
    codigo=request.POST['codigo']
    nombre=request.POST['nombre']
    tipo=request.POST['tipo']
    imagen = request.FILES.get('imagen', None)
    precio = request.POST['precio']

    productos = get_object_or_404(Productos, codigo=codigo)
    productos.nombre= nombre
    productos.tipo = tipo
    productos.precio = precio
    if imagen:
        productos.imagen = imagen
    productos.save()
    messages.success(request,'Producto Actualizado!')
    return redirect('/')

@login_required
@user_passes_test(es_admin)
def eliminacionProducto(request,codigo):
    productos = get_object_or_404(Productos, codigo=codigo)
    productos.delete() 
    messages.success(request,'Producto Eliminado!')
    return redirect('/')

#vistas categorias 
@login_required
@user_passes_test(es_admin)
def gestionCategorias(request):
    categorias = Categoria.objects.all()
    return render(request, "gestionCategorias.html", {"categorias": categorias})

@login_required
@user_passes_test(es_admin)
def registrarCategoria(request):
    nombre = request.POST['nombre']
    codigo=request.POST['codigo']

    Categoria.objects.create(nombre=nombre, codigo=codigo)
 
    messages.success(request, 'Categoría Registrada!')
    return redirect('/categorias')

@login_required
@user_passes_test(es_admin)
def vistaAgregarCategoria(request):
    return render(request, 'agregarCategoria.html')

@login_required
@user_passes_test(es_admin)
def edicionCategoria(request, codigo):
    categoria = get_object_or_404(Categoria, codigo=codigo)
    return render(request, "edicionCategoria.html", {"categoria": categoria})

@login_required
@user_passes_test(es_admin)
def eliminacionCategoria(request,codigo):
    categoria = get_object_or_404(Categoria, codigo=codigo)
    categoria.delete() 
    messages.success(request,'Categoria Eliminada!')
    return redirect('/categorias')

#vistas clientes 
@login_required
@user_passes_test(es_admin)
def gestionClientes(request):
    clientes = Clientes.objects.all()
    return render(request, "gestionClientes.html",{"clientes" : clientes})

@login_required
@user_passes_test(es_admin)
def vistaAgregarCliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente agregado')
            return redirect('/clientes')
    else:
        form = ClienteForm()
    return render(request, 'agregarCliente.html', {'form': form})
     
@login_required
@user_passes_test(es_admin)
def edicionCliente(request,codigo):
    cliente = get_object_or_404(Clientes, codigo=codigo)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado correctamente')
            return redirect('/clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'edicionCliente.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def eliminacionCliente(request, codigo):
    cliente = get_object_or_404(Clientes, codigo=codigo)
    cliente.delete()
    messages.success(request, 'Cliente eliminado')
    return redirect('/clientes')

#vistas pedidos 
@login_required
@user_passes_test(es_admin)
def gestionPedidos(request):
    pedidos = Pedidos.objects.all()
    return render(request, "gestionPedidos.html", {"pedidos": pedidos})

@login_required
@user_passes_test(es_admin)
def vistaAgregarPedido(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        codigo = request.POST['codigo']
        cliente = get_object_or_404(Clientes, codigo=request.POST['cliente'])
        fecha_pedido = request.POST['fecha_pedido']
        estado = request.POST['estado']

        # Crear un nuevo pedido
        nuevo_pedido = Pedidos(codigo=codigo, cliente=cliente, fecha=fecha_pedido, estado=estado)
        nuevo_pedido.save()

        messages.success(request, 'Pedido agregado correctamente.')
        return redirect('gestion_pedidos')

    # GET: mostrar formulario con datos iniciales
    clientes = Clientes.objects.all()
    estados = [
        ('Pendiente', 'Pendiente'),
        ('Procesado', 'Procesado'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    ]
    return render(request, 'agregarPedidos.html', {
        'clientes': clientes,
        'estados': estados
    })

@login_required
@user_passes_test(es_admin)
def edicionPedido(request, codigo):
    pedido = get_object_or_404(Pedidos, codigo=codigo)

    if request.method == 'POST':
        # Campos del pedido
        pedido.estado = request.POST['estado']
        pedido.fecha  = request.POST['fecha_pedido']
        pedido.save()
        messages.success(request, 'Pedido actualizado correctamente.')
        return redirect('gestion_pedidos')

    estados = [
        ('Pendiente', 'Pendiente'),
        ('Procesado', 'Procesado'),
        ('Enviado', 'Enviado'),
        ('Entregado', 'Entregado'),
    ]
    # GET: mostrar formulario con valores iniciales
    clientes  = Clientes.objects.all()
    productos = Productos.objects.all()
    return render(request, 'edicionPedidos.html', {
        'pedido':    pedido,
         'estados': estados,
    })

@login_required
@user_passes_test(es_admin)
def eliminacionPedido(request,codigo):
    pedido = get_object_or_404(Pedidos, codigo=codigo)
    pedido.delete()
    messages.success(request, 'Pedido eliminado')
    return redirect('/pedidos')

def home_ecommerce(request):
    return render(request, 'home_ecommerce.html')

def productos_por_categoria(request, codigo):
    categoria = get_object_or_404(Categoria, codigo=codigo)
    productos = Productos.objects.filter(categoria=categoria)
    return render(request, "productos_por_categoria.html", {
        "categoria": categoria,
        "productos": productos
    })

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        correo = request.POST['correo']
        password = request.POST['password']
        nombre = request.POST['nombre']
        apellidopaterno = request.POST['apellidopaterno']
        apellidomaterno = request.POST['apellidomaterno']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        # Crear usuario
        user = User.objects.create_user(username=username, email=correo, password=password)
        # Generar código único
        codigo = get_random_string(length=6).upper()

        # Crear cliente vinculado
        cliente = Clientes.objects.create(
            user=user,
            codigo=codigo,
            nombre=nombre,
            apellidopaterno=apellidopaterno,
            apellidomaterno=apellidomaterno,
            correo=correo,
            telefono=telefono
        )

        # Iniciar sesión
        login(request, user)
        return redirect('login')

    return render(request, 'registro.html')

class LoginClienteView(LoginView):
    template_name = 'login.html'  #personalizado

def agregar_al_carrito(request, codigo):
    carrito = request.session.get('carrito', {})

    #si existe aumenta cant
    if codigo in carrito:
        carrito[codigo] += 1
    else:
        carrito[codigo] = 1

    request.session['carrito'] = carrito
    return redirect('ver_carrito') 



def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for codigo, cantidad in carrito.items():
        try:
            producto = get_object_or_404(Productos, codigo=codigo)
            subtotal = producto.precio * cantidad
            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })
            total += subtotal
        except Productos.DoesNotExist:
            pass  

    return render(request, 'carrito.html', {
        'productos': productos,
        'total': total
    })


@login_required
def pagar_carrito(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        if not carrito:
            messages.error(request, 'Tu carrito está vacío.')
            return redirect('ver_carrito')

        user = request.user
        try:
            cliente = Clientes.objects.get(user=user)
        except Clientes.DoesNotExist:
            messages.error(request, 'Debes estar registrado como cliente para realizar un pedido.')
            return redirect('login')

        # Genera codigou para pedido
        codigo = f"PD{random.randint(1000, 9999)}"

       #crea pedido
        pedido = Pedidos.objects.create(
            codigo=codigo,
            cliente=cliente,
            estado='Procesado',
        )

        request.session['carrito'] = {}

        messages.success(request, '¡Pedido realizado exitosamente!')
        return redirect('ver_carrito')

    return redirect('ver_carrito')

def eliminar_del_carrito(request, codigo):
    carrito = request.session.get('carrito', {})
    
    if codigo in carrito:
        del carrito[codigo]
        request.session['carrito'] = carrito
        messages.success(request, 'Producto eliminado del carrito.')
    
    return redirect('ver_carrito')
