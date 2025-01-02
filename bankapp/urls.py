# from django.urls import path,include
# from .views import *
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'bank',BankViewSet,basename='bank'),
# router.register(r'statement_type', StatementTypeViewSet, basename='statement_type')
# urlpatterns = [
#     path('api/', include(router.urls)),
#     path('', index, name='index'),
#     path('upload/', upload_file, name='upload_file'),
#     path('account-info/', get_account_info, name='get_account_info'),
#     path('transactions/', get_transactions, name='get_transactions')
# ]
from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bank', BankViewSet, basename='bank')
router.register(r'statement_type', StatementTypeViewSet, basename='statement_type')

urlpatterns = [
    path('api/', include(router.urls)),
    path('', statement_pdf, name='statement_pdf'),
    path('upload_pdf/', upload_pdf, name='upload_pdf')
]


