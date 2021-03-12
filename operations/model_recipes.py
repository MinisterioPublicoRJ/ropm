from model_bakery.recipe import Recipe

from operations.models import Operacao


op_recipe_with_occurence = Recipe(
    Operacao,
    houve_ocorrencia_operacao=None,
    rg_pm_comandante_operacao="12345",
    rg_pm_condutor_ocorrencia="67890",
    registro_ocorrencia="034-00001/2019",
    tipo_operacao="Pl",
    numero_ordem_operacoes="123456",
    _fill_optional=True
)

op_recipe_without_occurence = Recipe(
    Operacao,
    houve_ocorrencia_operacao=None,
    _fill_optional=True
)
