from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from operations.models import Operacao


class CreateGeneralInfo(APIView):
    permission_classes = [IsAuthenticated]

    def create_object(self, user, id_):
        obj, _ = Operacao.objects.get_or_create(identificador=id_, usuario=user)
        return obj

    def post(self, request, *args, **kwargs):
        form_uuid = kwargs.get("form_uuid")
        self.create_object(self.request.user, form_uuid)
        return Response()
