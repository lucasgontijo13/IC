from .models import Cliente

def cliente_context(request):
    if request.user.is_authenticated:
        cliente_id = request.session.get('cliente_id')
        if cliente_id:
            try:
                cliente = Cliente.objects.get(id=cliente_id)
                return {'cliente': cliente}
            except Cliente.DoesNotExist:
                return {}
    return {}
