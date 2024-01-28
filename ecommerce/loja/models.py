from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return self.nome
    
class Produto(models.Model):
    nome = models.CharField(max_length=200, null=True)
    preco = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.nome
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False, null=True, blank=False)
    transacao_id = models.CharField(max_length=200, null=True)

    def __str__(self) -> str:
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        itens_pedido = self.itempedido_set.all()
        for i in itens_pedido:
            if i.produto.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        pedidoitem = self.itempedido_set.all()
        total = sum([item.get_total for item in pedidoitem])
        return total
    
    @property
    def get_cart_items(self):
        pedidoitem = self.itempedido_set.all()
        total = sum([item.quantidade for item in pedidoitem])
        return total

class ItemPedido(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    quantidade = models.IntegerField(default=0, null=True, blank=True)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.produto.preco * self.quantidade
        return total

class EnderecoEntrega(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    endereco = models.CharField(max_length=200, null=False)
    cidade = models.CharField(max_length=200, null=False)
    estado = models.CharField(max_length=200, null=False)
    cep = models.CharField(max_length=200, null=False)
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.endereco
