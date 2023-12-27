from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions, status, viewsets
from django.contrib.auth import login, logout
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    CollectionSerializer,
    BookmarkCreateSerializer,
    BookmarkSerializer,
)
from .models import Collection, Bookmark, User
from .bookmark_service.utils import extract_metadata



class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [
                            permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,
                        ]


    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user

        super().perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class BookmarkViewSet(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    permission_classes = [
                            permissions.IsAuthenticatedOrReadOnly,
                            IsOwnerOrReadOnly,
                        ]

    def get_serializer_class(self):
        if self.action == 'create':
            return BookmarkCreateSerializer
        return BookmarkSerializer



    def perform_create(self, serializer):
        url = self.request.data.get('link')
        metadata = extract_metadata(url)

        if metadata:
            serializer.validated_data['user'] = self.request.user
            serializer.validated_data['collection'] = self.request.data.get("collection")
            serializer.validated_data['title'] = metadata.get('title', ' ')
            serializer.validated_data['description'] = metadata.get('description', ' ')
            serializer.validated_data['image_preview'] = metadata.get('image', ' ')

        super().perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    http_method_names = ["post", "options"]

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()
      
        return Response(
            {"email": user.email},
            status=status.HTTP_201_CREATED,
        )



class LoginViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "options"]
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def create(self, request) -> Response:
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        login(request, user)

        return Response(
            {
                "user_info": user.email,
            },
            status=status.HTTP_202_ACCEPTED,
        )


class LogoutViewSet(viewsets.ViewSet):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def create(self, request) -> Response:
        logout(request)

        return Response({"code": status.HTTP_200_OK})

