from django.core.management.base import BaseCommand
from django.utils import timezone

from operations.models import Operacao


LOCAL_ZONE = timezone.get_current_timezone()


class Command(BaseCommand):
    help = "Mostra o histórico de alterações de uma operação"

    def add_arguments(self, parser):
        parser.add_argument("identificador")

    def handle(self, *args, **kwargs):
        identificador = kwargs["identificador"]
        op = Operacao.objects.get(identificador=identificador)
        history = op.history.all()
        last_change = history[0]

        dt_msg = "\u001b[32mAlteração feita em: {data} por {usuario}\033[0m"
        log_msg = "\t{field}: {old} ------> {new}"
        for state in history[1:]:
            delta = last_change.diff_against(state)
            if delta.changes:
                print(dt_msg.format(
                    data=state.history_date.astimezone(LOCAL_ZONE),
                    usuario=state.history_user.username
                ))
            for change in delta.changes:
                msg = log_msg.format(
                    field=change.field.upper(),
                    old=change.old or "-",
                    new=change.new or "-"
                )
                print(msg)
