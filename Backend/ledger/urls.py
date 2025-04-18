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
    path('api/change_balance/<int:account_id>/<str:amount>/', views.change_balance, name="change_balance"),
    path('api/transactions/create/<int:account_id>/<str:amount>/<str:description>/', views.create_transaction,
         name='create_transaction'),
    path('api/transactions/<int:account_id>/', views.get_transaction_history, name='get_transaction_history'),
    path('api/accounts/<int:account_id>/update_balance/<str:new_balance>/', views.update_balance,
         name='update_balance'),

]