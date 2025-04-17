from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'accounts', views.AccountViewSet)
router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    # API endpoints via DRF router
    path('api/', include(router.urls)),

    # Existing HTML endpoints
    path("", views.index, name="index"),
    path("accounts/", views.accounts, name="accounts"),
]
