from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateUpdateViewSet(
    mixins.UpdateModelMixin, mixins.CreateModelMixin, GenericViewSet
):
    pass
