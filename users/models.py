from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    TIPO_INSTITUICAO = [
        ("PM", "Polícia Militar"),
        ("PC", "Polícia Civil"),
        ("MPRJ", "MPRJ"),
    ]

    instituicao = models.CharField(
        "Instituição",
        choices=TIPO_INSTITUICAO,
        max_length=10
    )
