from django.urls import path

from day5 import views

urlpatterns = [
    # path('books/',views.BookAPIView.as_view()),
    # path('books/<str:id>/',views.BookAPIView.as_view()),

    path("gen/", views.BookGenericAPIView.as_view()),
    path("gen/<str:id>/", views.BookGenericAPIView.as_view()),

    path("mix/", views.BookGenericMixinView.as_view()),
    path("mix/<str:id>/", views.BookGenericMixinView.as_view()),

    path("set/", views.BookModelViewSet.as_view({"post": "user_login", "get": "get_user_count"})),
    path("set/<str:id>/", views.BookModelViewSet.as_view({"post": "user_login", "get": "get_user_count"})),
]