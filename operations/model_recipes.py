from model_bakery.recipe import Recipe

from operations.models import Operacao


REGISTRO_OCORRENCIA = "034-00001/2019"


op_recipe_with_occurence = Recipe(
    Operacao,
    houve_ocorrencia_operacao=None,
    rg_pm_comandante_operacao="12345",
    rg_pm_condutor_ocorrencia="67890",
    registro_ocorrencia=REGISTRO_OCORRENCIA,
    tipo_operacao="Pl",
    numero_ordem_operacoes="123456",
    _fill_optional=True
)

op_recipe_without_occurence = Recipe(
    Operacao,
    houve_ocorrencia_operacao=None,
    _fill_optional=True
)


op_recipe_with_ocurrence_data = Recipe(
    Operacao,
    houve_ocorrencia_operacao=True,
    boletim_ocorrencia_pm="123456",
    registro_ocorrencia=REGISTRO_OCORRENCIA,
    nome_condutor_ocorrencia="nome",
    rg_pm_condutor_ocorrencia="123456",
    posto_condutor_ocorrencia=Operacao.POSTO_COMANDANTE[0][0],
    houve_apreensao_drogas=True,
    numero_armas_apreendidas=2,
    numero_fuzis_apreendidos=2,
)

op_recipe_without_ocurrence_data = Recipe(
    Operacao,
    houve_ocorrencia_operacao=True
)
