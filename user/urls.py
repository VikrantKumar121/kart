from django.urls import path
from .views import register, login, logout, activate, dashboard, forgot_password, resetpassword_validate, reset_password, my_order, edit_profile, change_password, order_detail

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

    path('my_order/', my_order, name = 'my_order' ),
    path('edit_profile/', edit_profile, name = 'edit_profile' ),
    path('change_password/', change_password, name = 'change_password' ),
    path('order_detail/<int:order_id>', order_detail, name = 'order_detail' ),

]
