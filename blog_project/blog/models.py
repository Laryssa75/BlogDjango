from django.db import models
from django.contrib.auth.models import user
from django.utils import timezone
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categorias"
        
    def __str__(self):
        return self.nome
    
class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome
    
class Post(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho')
        ('publicado', 'Publicado')
    )
    
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    imagem = models.ImageField(upload_to='posts/', blank=True, null=True)
    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rascunho')
    
    class Meta:
        ordering = ['-criado_em']
        
    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        return reverse("post_detalhe", kwargs={"slug": self.slug})
    
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cometarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    conteudo = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['criado_em']
        
    def __str__(self):
        return f'Comentario de {self.autor} em {self.post}'
    
    