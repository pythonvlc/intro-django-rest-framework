from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Todo
from .serializers import TodoSerializer
from .permissions import IsOwnerOrDeny


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrDeny)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user, done=False)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TodoDoneViewSet(viewsets.ViewSet):

    def done(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        todo = get_object_or_404(Todo, pk=pk, owner=request.user)

        todo.mark_as_done()

        return Response(status=status.HTTP_204_NO_CONTENT)


done = TodoDoneViewSet.as_view({'patch': 'done'})
