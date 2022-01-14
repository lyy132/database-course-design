from django.urls import path
from . import views
app_name='manage_system'
urlpatterns = [

    path('', views.login, name='login'),
    path('index/',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('customer/<int:pIndex>',views.customer_show,name='customer_show'),
    path('customer/add',views.customer_add,name='customer_add'),
    path('customer_insert/',views.customer_insert,name='customer_insert'),
    path('customer/edit/<int:uid>',views.customer_edit,name="customer_edit"),
    path('customer_update/<int:uid>',views.customer_update,name="customer_update"),    
    path('customer_delete/<int:uid>',views.customer_delete,name='customer_delete'),

    path('storage/<int:pIndex>',views.storage_show,name='storage_show'), 
    path('storge/edit/<int:sid>',views.storage_edit,name='storage_edit'),   
    path('storage_update/<int:sid>',views.storage_update,name="storage_update"),
    path('storage_delete/<int:sid>',views.storage_delete,name='storage_delete'),
    path('storage/add',views.storage_add,name='storage_add'),
    path('storage_insert',views.storage_insert,name='storage_insert'),    


    path('user_manage/<int:pIndex>',views.user_manage,name='user_manage'),
    path('user/edit/<int:uid>',views.user_edit,name='user_edit'),
    path('user_update/<int:uid>',views.user_update,name="user_update"),
    path('user_delete/<int:uid>',views.user_delete,name="user_delete"),
    path('user/add',views.user_add,name='user_add'),
    path('user_insert',views.user_insert,name="user_insert"),

    path('product/<int:pIndex>',views.product_show,name='product_show'),
    path('product/add',views.product_add,name='product_add'),    
    path('product_insert/',views.product_insert,name="product_insert"),
    path('product/edit/<int:pid>',views.product_edit,name='product_edit'),
    path('product_update/<int:pid>',views.product_update,name="product_update"),
    path('product_delete/<int:pid>',views.product_delete,name="product_delete"),

    path('pwd_reset/',views.forget_pwd,name="pwd_reset"),
    path('pwd_resetfinally/',views.resetpassword,name="resetpwd"),
    path('pwd_resetnew/',views.forget_password,name="pwd_resetnew"),

]