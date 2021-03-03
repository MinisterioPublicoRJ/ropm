from model_bakery.recipe import Recipe

from operations.models import Operacao


op_recipe_with_occurence = Recipe(
    Operacao,
    houve_ocorrencia_operacao=None,
    _fill_optional=True
)

op_recipe_without_occurence = Recipe(
    Operacao,
    houve_ocorrencia_operacao=None,
    _fill_optional=True
)
