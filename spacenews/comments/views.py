from rest_framework import mixins, viewsets

from .models import Comment
from .permissions import CommentPermission
from .serializers import CommentSerializer


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):

    # we don't want to allow creating new comments, handled under posts

    queryset = Comment.objects.select_related('author').order_by('-created')
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission, )
