from django.urls import path

from homeworkday05 import views

urlpatterns = [
 path('teacher/',views.TeacherGenMixView.as_view()),
 path('teacher/<str:id>/',views.TeacherGenMixView.as_view()),

 path('teachers/',views.TeacherGenMixViews.as_view()),
 path('teachers/<str:id>/',views.TeacherGenMixViews.as_view()),

 path('teacherset/',views.TeacherModelViewSet.as_view({'patch':'patch'})),
 path('teacherset/<str:id>/',views.TeacherModelViewSet.as_view({'patch':'patch'})),


 path('user/',views.UserModelViewSet.as_view({'post':'user_register'})),
 path('users/',views.UseViewSet.as_view({'post':'user_login'})),

]