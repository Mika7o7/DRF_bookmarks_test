from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
                        CollectionViewSet,
                        BookmarkViewSet,
                        RegisterViewSet,
                        LoginViewSet,
                        LogoutViewSet
                    )

router = DefaultRouter()
router.register('collections', CollectionViewSet, basename="collections")
router.register('bookmarks', BookmarkViewSet, basename="bookmarks")
router.register("auth/register", RegisterViewSet, basename="register")
router.register("auth/login", LoginViewSet, basename="login")
router.register("auth/logout", LogoutViewSet, basename="logout")

urlpatterns = [
    path('', include(router.urls)),
]

   