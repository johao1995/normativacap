import uuid
from django.db import models
from .choices import *
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import User
from normas.models import Master_Normas
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect

def upload_file(instance, filename):
    ext = filename.split('.')[-1]
    return 'pdf/{}'.format(instance.file)

def upload_signature(instance, filename):
    ext = filename.split('.')[-1]
    return 'signatures/{}.{}'.format(instance.file, ext)

def upload_photos(instance, filename):
    ext = filename.split('.')[-1]
    return 'photos/{}.{}'.format(instance.identity, ext)



"""

 * TABLAS GENERALES 

"""

class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        help_text='Usuario', null=True, blank=True,
        verbose_name='Usuario')
    first_surname = models.CharField(max_length=50, blank=True,
        help_text='Apellido Paterno',
        verbose_name='Apellido Paterno')
    second_surname = models.CharField(max_length=50, blank=True,
        help_text='Apellido Materno',
        verbose_name='Apellido Materno')
    names = models.CharField(max_length=50, blank=False,
        help_text='Nombres O Razón Social',
        verbose_name='Nombres')
    full_name = models.CharField(max_length=200, blank=False,default='Nombre completo',
        help_text='Apellidos y Nombres',
        verbose_name='Apellidos y Nombres')
    person_type = models.CharField(max_length=1, default='N',
        help_text='Tipo de Persona', choices=PERSON_TYPE_CHOICES,
        verbose_name='Tipo de Persona', blank=False)
    identity = models.CharField(max_length=11, blank=True,
        help_text='DNI o RUC',
        verbose_name='Documento de Identidad')
    profession = models.CharField(max_length=1,
        help_text='Profesión', choices=PROFESSION_CHOICES,
        verbose_name='Profesión', blank=True)
    mobile = models.CharField(max_length=12, blank=True,
        help_text='Número de Teléfono Celular',
        verbose_name='Celular')
    phone = models.CharField(max_length=10, blank=True,
        help_text='Número de Teléfono Fijo o de Oficina',
        verbose_name='Teléfono')
    email = models.EmailField(max_length=50, blank=False,default='correo@dominio.com',
        help_text='Correo Electrónico',
        verbose_name='Email')
    tuition = models.PositiveIntegerField(null=True, blank=True,
        help_text='Colegiatura',
        verbose_name='Colegiatura')
    secret_code = models.PositiveIntegerField(null=True, blank=True,
        help_text='Código Secreto de Arquitecto',
        verbose_name='Código Secreto de Arquitecto')
    address = models.CharField(max_length=200, blank=True,
        help_text='Dirección',
        verbose_name='Dirección')
    # is_signature_validated = models.BooleanField(blank=True,
    #     help_text='Marcado si la firma está validada por el CAP',
    #     verbose_name='Firma Validada')
    # signature = models.ImageField(
    #     upload_to=upload_signature, blank=True,
    #     help_text='Suba una imágen escaneada de su sello y firma, los cuales será utilizados como validación de las solicitudes que realice através del portal',
    #     verbose_name='Firma')
    area_interest = models.CharField(max_length=200, blank=True,
        help_text='areas de interes',
        verbose_name='areas de interes')
    institution = models.CharField(max_length=200, blank=True,
        help_text='Institucion',
        verbose_name='Institucion')
    photo = models.ImageField(
        upload_to=upload_photos, blank=True, null=True,
        help_text='Suba una fotografía en tamaño pasaporte o carnet',
        verbose_name='Fotografía')
    register_date_time = models.DateTimeField(
        blank=False, null=False, auto_now_add=True,
        help_text='Fecha de Registro',
        verbose_name='Fecha de Registro')

    
    def __str__(self):
        return self.full_name 
 
    class Meta:
        ordering = ['created']
         
    class Meta:  
        db_table = "member"

    class Meta:
        verbose_name_plural = 'Relacion de Miembros'

class Plan(models.Model):
    
    planame = models.CharField(max_length=200, blank=False,
        help_text='Nombre de Plan',
        verbose_name='Plan')      
    cost = models.DecimalField(max_digits = 10,decimal_places = 2)
    validity_date_start = models.DateField(
        blank=False, null=False, auto_now_add=False,
        help_text='Fecha',
        verbose_name='Fecha Inicio')
    validity_date_finish = models.DateField(
        blank=False, null=False, auto_now_add=False,
        help_text='Fecha',
        verbose_name='Fecha Fin')
    register_date_time = models.DateField(
        blank=False, null=False, auto_now_add=True,
        help_text='Fecha de Registro',
        verbose_name='Fecha de Registro')
    
    class Meta:
        verbose_name_plural = 'Planes de Suscripcion'

    def __str__(self):
        return self.planame 

class Control_payment(models.Model):
    
    member = models.OneToOneField(
        Member, on_delete=models.CASCADE,
        help_text='Miembros', null=True, blank=True,
        verbose_name='Miembros')
    id_plan = models.OneToOneField(
        Plan, on_delete=models.CASCADE,
        help_text='Plan Suscrito', null=True, blank=True,
        verbose_name='Plan de Suscripcion')        
    pay_method = models.CharField(max_length=1,
        help_text='Metodo de Pago', choices=METODPAY_CHOICES,
        verbose_name='Metodo de Pago', blank=True)
    pay_import = models.DecimalField(max_digits = 10,decimal_places = 2,
        help_text='Importe Pagado',
        verbose_name='Importe Pagado')  
    validity_date_start = models.DateField(
        blank=False, null=False, auto_now_add=False,
        help_text='Fecha',
        verbose_name='Fecha Inicio')
    validity_date_finish = models.DateField(
        blank=False, null=False, auto_now_add=False,
        help_text='Fecha',
        verbose_name='Fecha Fin')
    register_date_time = models.DateTimeField(
        blank=False, null=False, auto_now_add=True,
        help_text='Fecha de Registro',
        verbose_name='Fecha de Registro')


        
    class Meta:
        verbose_name_plural = 'Control de Pagos'

class Policies_usage(models.Model):
    
    title = models.CharField(max_length=200, blank=False,
        help_text='Titulo de Consulta',
        verbose_name='Titulo de Consulta')      
    message = models.TextField(blank=False,
        help_text='Respuesta',
        verbose_name='Respuesta')      
    platform =  models.CharField(max_length=1,
        help_text='Plataforma', choices=PLATAFORMA_TYPE_CHOICES,
        verbose_name='Plataforma', blank=False) 
    validity_date_start = models.DateField(
        blank=False, null=False, auto_now_add=False,
        help_text='Fecha',
        verbose_name='Fecha Inicio')
    validity_date_finish = models.DateField(
        blank=False, null=False, auto_now_add=False,
        help_text='Fecha',
        verbose_name='Fecha Fin')
    register_date_time = models.DateTimeField(
        blank=False, null=False, auto_now_add=True,
        help_text='Fecha de Registro',
        verbose_name='Fecha de Registro')

    norma_name = models.ManyToManyField(Master_Normas,related_name="normas_rel") 

    class Meta:
        verbose_name_plural = 'Preguntas Frecuentes'


class UserToken(models.Model):
    token = models.UUIDField(primary_key=True, null=False, unique=True,
        default=uuid.uuid4, editable=False)
    user_profile = models.OneToOneField(
        Member, on_delete=models.CASCADE,
        help_text='Usuario', null=False,
        verbose_name='Usuario')

    class Meta:
        verbose_name_plural = 'Tokens'

    def get_confirm_link(self):
        print (self.token)
        #return reverse('sign_up', kwargs={'token': self.token})
        

    def get_password_reset_link(self):
        return reverse('password_reset_token', kwargs={'token': self.token})
 
#johao
class Register_Normativa(models.Model):
    norma=models.CharField(blank=False,null=False,max_length=200,verbose_name='Norma')
    name_denom = models.TextField(blank=False,null=False,verbose_name='Denominacion')
    base_legal=models.CharField(blank=False,null=False,max_length=200,verbose_name='Base Legal')
    fecha_publi = models.DateField(blank=False,null=False,verbose_name='Publicacion')
    tipo_norma=models.CharField(blank=False,null=False,max_length=200,
    verbose_name='Tipo de Norma')
    tipo_uso = models.CharField(blank=False,null=False,max_length=200,
    verbose_name='Tipo de Uso')
    document=models.FileField(upload_to='Document_normativa',verbose_name='Documentos')

    class Meta:
        verbose_name_plural='Normativas Registradas'
        db_table='register_normativa'
    
class Register_Palabraclave(models.Model):
    name = models.TextField(blank=False,null=False,verbose_name='Nombre Palabra Clave')
    normativa = models.ForeignKey(Register_Normativa,verbose_name='Normativa',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='Palabras Clave'
        db_table='register_palabclave'
    

#end

"""

 * TABLAS NORMAS 
 

"""

"""
"Registartions
 Attributes of Registartions are registration_id,registration_user_id,registration_name, registration_type,registration_number, registration_date,registration_description"

"Posts :
 post_id,post_user_id,post_title,post_type, post_description"

"Replies :
 replies_id, replies_user_id,replies_title, replies_type,replies_description"

"Polls Entity : Attributes of Polls are poll_id,poll_name, pon_type, poll_description"
https://github.com/mdn/django-diy-blog/blob/master/blog/models.py
"""
