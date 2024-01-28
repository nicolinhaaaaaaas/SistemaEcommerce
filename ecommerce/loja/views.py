from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
from django.views.decorators.csrf import csrf_exempt

def loja(request):

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        itens = pedido.itempedido_set.all()
        pedidoCarrinho = pedido.get_cart_items
    else:
        itens = []
        pedido = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        pedidoCarrinho = pedido['get_cart_items']

    produtos = Produto.objects.all()
    context = {'produtos': produtos, 'pedidoCarrinho': pedidoCarrinho}
    return render(request, 'loja/loja.html', context)

def carrinho(request):

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        itens = pedido.itempedido_set.all()
        pedidoCarrinho = pedido.get_cart_items
    else:
        itens = []
        pedido = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        pedidoCarrinho = pedido['get_cart_items']

    context = {'itens':itens, 'pedido':pedido, 'pedidoCarrinho': pedidoCarrinho}
    return render(request, 'loja/carrinho.html', context)

def checkout(request):

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        itens = pedido.itempedido_set.all()
        pedidoCarrinho = pedido.get_cart_items
    else:
        itens = []
        pedido = {'get_cart_total':0, 'get_cart_items':0}
        pedidoCarrinho = pedido['get_cart_items']

    context = {'itens':itens, 'pedido':pedido, 'pedidoCarrinho': pedidoCarrinho}
    return render(request, 'loja/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    produtoId = data['produtoId']
    action = data['action']

    print('Action:', action)
    print('Produto:', produtoId)

    cliente = request.user.cliente
    produto = Produto.objects.get(id=produtoId)
    pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)

    itemPedido, created = ItemPedido.objects.get_or_create(pedido=pedido, produto=produto)

    if action == 'add':
        itemPedido.quantidade = (itemPedido.quantidade + 1)
    elif action == 'remove':
        itemPedido.quantidade = (itemPedido.quantidade - 1)
    
    itemPedido.save()

    if itemPedido.quantidade <= 0:
        itemPedido.delete()

    return JsonResponse('Item adicionado', safe=False)

@csrf_exempt
def processOrder(request):
    id_transacao = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completo=False)
        total = float(data['form']['total'])
        pedido.transacao_id = id_transacao

        if total == pedido.get_cart_total:
            pedido.completo = True
        pedido.save()

        if pedido.shipping == True:
            EnderecoEntrega.objects.create(
                cliente=cliente,
                pedido=pedido,
                endereco=data['shipping']['endereco'],
                cidade=data['shipping']['cidade'],
                estado=data['shipping']['estado'],
                cep=data['shipping']['cep'],
            )
    else:
        print('Usuário não está logado')    
    return JsonResponse('Pagamento concluído', safe=False)