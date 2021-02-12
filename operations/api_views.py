from rest_framework.response import Response
from rest_framework.views import APIView


class CreateGeneralInfo(APIView):
    def post(self, request, *args, **kwargs):
        return Response()
