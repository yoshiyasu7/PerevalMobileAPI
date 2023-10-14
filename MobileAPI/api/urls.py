from django.urls import path
from .views import PerevalAPIViewSet, reverse_to_submit


urlpatterns = [
    path('', reverse_to_submit),
    path('submitData/', PerevalAPIViewSet.as_view({"post": "post", }), name='submitData'),
]
