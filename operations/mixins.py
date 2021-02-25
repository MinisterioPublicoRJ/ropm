from rest_framework import status
from rest_framework.response import Response


class AllowPUTAsCreateMixin:
    def update(self, request, *args, **kwargs):
        self.operacao = self.get_operation()
        instance = self.model_class.objects.get_obj_or_none(self.operacao)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_create_or_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        if instance is None:
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        return Response(serializer.data)

    def perform_create_or_update(self, serializer):
        serializer.save(operacao=self.operacao)
