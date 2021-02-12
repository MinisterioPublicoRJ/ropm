from django.db import models

from users.models import User


class Operacao(models.Model):
    identificador = models.UUIDField(unique=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    editado = models.BooleanField("Editado", default=False)

    class Meta:
        db_table = "operacao"
        verbose_name = "operação"
        verbose_name_plural = "operações"


class InformacaoGeralOperacao(models.Model):
    operacao = models.OneToOneField(Operacao, on_delete=models.CASCADE)

    data = models.DateField("Data")
    hora = models.TimeField("Hora")

    localidade = models.CharField("Localidade", max_length=255)
    municipio = models.CharField("Município", max_length=255)
    bairro = models.CharField("Bairro", max_length=255)
    endereco_referencia = models.CharField("Endereço de referência", max_length=255)
    coordenadas_geo = models.CharField("Referência geográfica", max_length=100, blank=True)
    batalhao_responsavel = models.CharField("Batalhão Responsável", max_length=255)

    class Meta:
        db_table = "informacao_geral_operacao"
        verbose_name = "informação geral de operação"
        verbose_name_plural = "informações gerais de operação"


class InformacaoOperacionalOperacao(models.Model):
    POSTO_COMANDANTE = [
        ("Cel", "Coronel"),
        ("Ten Cel", "Tenente Coronel"),
        ("Maj", "Major"),
        ("Cap", "Capitão"),
        ("1 Ten", "Primeiro Tenente"),
        ("2 Ten", "Segundo Tenente"),
        ("Subten", "Subtenente"),
        ("1 Sgt", "Primeiro Sargento"),
        ("2 Sgt", "Segundo Sargento"),
        ("3 Sgt", "Terceiro Sargento"),
        ("Cb", "Cabo"),
        ("Sd", "Soldado"),
    ]
    TIPO_OPERACAO = [
        ("Pl", "Planejada"),
        ("Em", "Emergencial"),
    ]
    TIPO_ACAO_REPRESSIVA = [
        ("AREP I", "AREP I"),
        ("AREP II", "AREP II"),
        ("AREP III", "AREP III"),
        ("AREP IV", "AREP IV"),
    ]

    operacao = models.OneToOneField(Operacao, on_delete=models.CASCADE)
    unidade_responsavel = models.CharField("Unidade operacional responsável", max_length=255)
    apoio_outras_unidades = models.BooleanField("Recebeu apoio de outras unidades")
    unidade_apoiadora = models.CharField("Unidade Apoiadora", max_length=255, blank=True)
    nome_comandante = models.CharField("Nome do Comandante", max_length=255)
    rg_pm_comandante = models.CharField("RG PM do Comandante", max_length=10)
    posto_comandante = models.CharField(
        "Posto|Graduação do Comandante",
        choices=POSTO_COMANDANTE,
        max_length=100
    )
    tipo_operacao = models.CharField(
        "Tipo de operação",
        choices=TIPO_OPERACAO,
        max_length=10
    )
    tipo_de_acao_repressiva = models.CharField(
        "Tipo de ação repressiva",
        choices=TIPO_ACAO_REPRESSIVA,
        max_length=15
    )
    objetivo_operacao = models.CharField("Objetivo da operação", max_length=100)
    numero_policiais_mobilizados = models.PositiveIntegerField(
        "Número de policiais mobilizados"
    )

    class Meta:
        db_table = "informacao_operacional_operacao"
        verbose_name = "informção operacional da operação"
        verbose_name_plural = "informações operacionais da operação"
