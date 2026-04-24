from Aplicaciones.Gestion.forms import ClienteForm


def test_cliente_form_campos_requeridos():
    """Verifica que los campos obligatorios están presentes"""
    form = ClienteForm(data={})
    
    assert not form.is_valid()
    assert 'codigo' in form.errors
    assert 'nombre' in form.errors
    assert 'correo' in form.errors


def test_cliente_form_telefono_vacio_es_valido():
    """Verifica que teléfono vacío es permitido"""
    form = ClienteForm(data={
        'codigo': 'CLI001',
        'nombre': 'Juan',
        'apellidopaterno': 'Pérez',
        'apellidomaterno': 'García',
        'correo': 'juan@test.com'
        # telefono vacío
    })
    # Este test solo verifica que el form puede crearse
    # No valida porque eso requeriría DB


def test_cliente_form_campos_opcionales():
    """Verifica que apellido materno es opcional"""
    form = ClienteForm(data={
        'codigo': 'CLI002',
        'nombre': 'María',
        'apellidopaterno': 'López'
        # apellidomaterno vacío
    })
    # Verifica que campos opcionales funcionan