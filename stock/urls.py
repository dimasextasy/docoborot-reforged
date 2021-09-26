from django.urls import path
from .views import (
    objects_list_view,
    objects_create_view,
    deal_create_view,
    deal_product_create_view,
    objects_update_view,
    objects_delete_view,
    deal_list_view,
    generate_report_view,
    verify_signatyre_view
)

urlpatterns = [
    path('deal/', deal_list_view),
    path('deal/new/', deal_create_view),
    path('deal/<int:id>/new-product/', deal_product_create_view),
    path('<str:object_name>/', objects_list_view),
    path('<str:object_name>/new/', objects_create_view),
    path('<str:object_name>/<int:id>/edit/', objects_update_view),
    path('<str:object_name>/<int:id>/delete/', objects_delete_view),
    path('deal/generate_report/', generate_report_view),
    path('deal/verify_signature/', verify_signatyre_view),
]
