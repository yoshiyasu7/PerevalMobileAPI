from django.urls import path
from .views import PerevalAPIViewSet, reverse_to_submit


urlpatterns = [
    path('', reverse_to_submit),
    path('submitData/', PerevalAPIViewSet.as_view({"post": "post", "get": "get_user_perevals", }), name='submitData'),
    path('submitData/<int:pk>', PerevalAPIViewSet.as_view({"get": "get_pereval", "patch": "edit_pereval", }),
         name='editData'),
]
