from django.urls import path
from .views import register, login, logout, activate, dashboard, forgot_password, resetpassword_validate, reset_password

urlpatterns = [
    path('register/', register, name= 'register'),
    path('login/', login, name= 'login'),
    path('logout/', logout, name= 'logout'),
    path('activate/<uidb64>/<token>/', activate, name= 'activate'),
    path('dashboard/', dashboard, name= 'dashboard'),
    path('', dashboard, name= 'dashboard'),
    path('forgotpassword/', forgot_password, name = 'forgotpassword' ),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name= 'resetpassword_validate'),
    path('resetpassword/', reset_password, name = 'resetpassword' ),

]
