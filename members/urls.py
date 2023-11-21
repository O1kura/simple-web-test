from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

router = routers.DefaultRouter()
router.register(r'members', views.MemberViewSet)
router.register(r'users', views.ListUsers)

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/add',views.add, name='add'),
    path('members/details/<int:id>',views.details,name='details'),
    path('testing/', views.testing, name='testing'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('api/', include(router.urls)),
    # path('api/example/', views.ExampleView.as_view()),
    path('api/members_view/', views.MembersView.as_view()),
    path('api/members_view/<int:id>', views.MemberDetailView.as_view()),
    path('api/login/', views.LoginView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]