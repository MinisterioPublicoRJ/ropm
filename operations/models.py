from django.conf import settings
from django.db import models
from django.urls import reverse

from users.models import User
from operations.exceptions import OperationNotCompleteException
from operations.mail import notifica_por_email


class InformacaoManager(models.Manager):
    def get_obj_or_none(self, usuario, identificador):
        try:
            obj = self.get(usuario=usuario, indentificador=identificador)
        except models.ObjectDoesNotExist:
            obj = None

        return obj


class Operacao(models.Model):
    n_sections = 8

    objects = InformacaoManager()

    SITUACAO_INCOMPLETO = "incompleto"
    SITUACAO_CSO = "completo sem ocorrencia"
    SITUACAO_CCO = "completo com ocorrencia"
    SITUACAO_CADASTRO = [
        (SITUACAO_INCOMPLETO, "Incompleto"),
        (SITUACAO_CSO, "Completo sem Ocorrência"),
        (SITUACAO_CCO, "Completo com Ocorrência"),
    ]
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

    secao_atual = models.PositiveIntegerField("Seção Atual", default=1)
    completo = models.BooleanField("Cadastro Completo", default=False)
    situacao = models.CharField(
        "Situação Cadastro",
        max_length=100,
        choices=SITUACAO_CADASTRO,
        default=SITUACAO_INCOMPLETO
    )

    identificador = models.UUIDField(unique=True, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    editado = models.BooleanField("Editado", default=False)
    data = models.DateField("Data", null=True, blank=True)
    hora = models.TimeField("Hora", null=True, blank=True)
    localidade = models.CharField("Localidade", max_length=255, null=True, blank=True)
    municipio = models.CharField("Município", max_length=255, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=255, null=True, blank=True)
    endereco_referencia = models.CharField("Endereço de referência", max_length=255, null=True, blank=True)
    coordenadas_geo = models.CharField("Referência geográfica", max_length=100, null=True, blank=True)
    batalhao_responsavel = models.CharField("Batalhão Responsável", max_length=255, null=True, blank=True)

    justificativa_excepcionalidade_operacao = models.TextField(
        "Justificativa da excepcionalidade da operação",
        null=True,
        blank=True
    )
    descricao_analise_risco = models.TextField(
        "Análise de riscos e medidas de controles de danos colaterais das operações e de disparos de confrontos",
        null=True,
        blank=True
    )

    unidade_responsavel = models.CharField("Unidade operacional responsável", max_length=255, null=True, blank=True)
    unidade_apoiadora = models.CharField("Unidade Apoiadora", max_length=255, null=True, blank=True)
    nome_comandante_operacao = models.CharField("Nome do Comandante", max_length=255, null=True, blank=True)
    rg_pm_comandante_operacao = models.CharField("RG PM do Comandante", max_length=10, null=True, blank=True)
    posto_comandante_operacao = models.CharField(
        "Posto|Graduação do Comandante",
        choices=POSTO_COMANDANTE,
        max_length=100,
        null=True
    )
    tipo_operacao = models.CharField(
        "Tipo de operação",
        choices=TIPO_OPERACAO,
        max_length=10,
        null=True
    )
    tipo_acao_repressiva = models.CharField(
        "Tipo de ação repressiva",
        choices=TIPO_ACAO_REPRESSIVA,
        max_length=15,
        null=True
    )
    numero_ordem_operacoes = models.CharField(
        "Número da ordem de operações no caso de operação planejada",
        max_length=100,
        null=True,
        blank=True
    )
    objetivo_estrategico_operacao = models.CharField(
        "Objetivo estratégico da operação",
        max_length=255,
        null=True,
        blank=True
    )
    numero_guarnicoes_mobilizadas = models.PositiveIntegerField(
        "Número de Guarnições mobilizadas",
        null=True,
        blank=True
    )
    numero_policiais_mobilizados = models.PositiveIntegerField(
        "Número de policiais mobilizados",
        null=True,
        blank=True
    )
    numero_veiculos_blindados = models.PositiveIntegerField(
        "Número de veículos blindados",
        default=0,
        blank=True
    )
    numero_aeronaves = models.PositiveIntegerField(
        "Número de aeronaves",
        default=0,
        blank=True
    )

    houve_confronto_daf = models.BooleanField(
        "Houve confronto com DAF?",
        null=True,
        blank=True,
    )
    houve_resultados_operacao = models.BooleanField(
        "Houve resultados na operação?",
        null=True,
        blank=True,
    )
    houve_ocorrencia_operacao = models.BooleanField(
        "Houve ocorrência na operação?",
        null=True,
        blank=True,
    )

    boletim_ocorrencia_pm = models.CharField(
        "Boletim de Ocorrência da Polícia Militar (BOPM)",
        max_length=100,
        null=True,
        blank=True,
    )
    registro_ocorrencia = models.CharField(
        "Registro de Ocorrência",
        max_length=100,
        null=True,
        blank=True,
    )
    nome_comandante_ocorrencia = models.CharField(
        "Nome do Comandante",
        max_length=100,
        null=True,
        blank=True,
    )
    rg_pm_comandante_ocorrencia = models.CharField(
        "RG PM do Comandante",
        max_length=100,
        null=True,
        blank=True,
    )
    posto_comandante_ocorrencia = models.CharField(
        "Posto|Graduação do Comandante",
        choices=POSTO_COMANDANTE,
        max_length=100,
        null=True
    )
    houve_apreensao_drogas = models.BooleanField(
        "Houve apreensão de Drogas?",
        null=True,
        blank=True,
    )
    numero_armas_apreendidas = models.PositiveIntegerField(
        "Número de armas apreendidas",
        null=True,
        blank=True
    )
    numero_fuzis_apreendidos = models.PositiveIntegerField(
        "Número de fuzis apreendidos",
        null=True,
        blank=True
    )
    numero_presos = models.PositiveIntegerField(
        "Número presos",
        null=True,
        blank=True
    )
    numero_adolescentes_apreendidos = models.PositiveIntegerField(
        "Número de adolescentes apreendidos",
        null=True,
        blank=True,
    )
    numero_policiais_feridos = models.PositiveIntegerField(
        "Número de policiais feridos",
        null=True,
        blank=True,
    )
    numero_mortes_policiais = models.PositiveIntegerField(
        "Número de mortes policiais",
        null=True,
        blank=True
    )
    numero_mortes_interv_estado = models.PositiveIntegerField(
        "Número de mortes por intervenção de agentes do Estado",
        null=True,
        blank=True
    )
    numero_civis_feridos = models.PositiveIntegerField(
        "Número de civis feridos",
        null=True,
        blank=True
    )
    numero_civis_mortos_npap = models.PositiveIntegerField(
        "Número de civis mortos – morte não provocada por agente policiais",
        null=True,
        blank=True
    )
    numero_veiculos_recuperados = models.PositiveIntegerField(
        "Número de veículos recuperados",
        null=True,
        blank=True
    )

    observations = models.TextField(
        "Observações gerais",
        null=True,
        blank=True
    )

    class Meta:
        db_table = "operacao"
        verbose_name = "operação"
        verbose_name_plural = "operações"

    @property
    def get_admin_url(self):
        path = reverse(
            "admin:%s_%s_change" % (self._meta.app_label, self._meta.model_name),
            args=[self.id]
        )
        return f"{settings.SITE_URL}{path}"

    def update_section(self, new_section):
        self.secao_atual = new_section
        self.save()

        return self.secao_atual

    def make_complete(self):
        if self.completo is False:
            self.completo = True
            self.notify_completion()

        self.situacao = self.SITUACAO_CSO
        if self.houve_ocorrencia_operacao is True:
            self.situacao = self.SITUACAO_CCO

        self.save()

    def notify_completion(self):
        if self.completo is False:
            raise OperationNotCompleteException

        if not settings.DEBUG:
            notifica_por_email(self)
