from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    ROLE = (
        ('gestor_TI', 'Gestor de TI'),
        ('docente', 'Docente'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE, default='user')

    # Minimal attributes expected when using a custom user model
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Django expects these class attributes for custom user models
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def encript_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        #compara 
        return check_password(raw_password, self.password)

    def __str__(self):
        return f'User: {self.username}, role={self.role}'

    # Methods expected by Django's auth checks
    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username