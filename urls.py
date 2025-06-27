from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.home, name='home'),
    #path('login/', views.login, name='login'),
    path('checkout/',views.checkout, name='checkout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('SignUp/', views.CustomerRegistrationView.as_view(), name='signup'),
     path('profile/', views.ProfileView.as_view(), name='profile'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path('About/',views.about, name='about'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart, name='pluscart'),
    path('minuscart/',views.minus_cart, name='minuscart'),
    path('removecart/',views.remove_cart, name='removecart'),
    path('allproducts/',views.allProducts, name='allProducts'),


    path('Barstool/',views.bar_stools, name='bar_stools'),
    path('Beds/',views.beds, name='beds'),
    path('Bedsidetable/', views.bed_side_table, name='bed-side-table'),
    path('BookShelf/',views.book_shelf, name='bookshelf'),
    path('Chaises/',views.chaises, name='chaises'),
    path('Chestdrawer/',views.chestdrawer, name='chestdrawer'),
    path('Coffeetable/',views.coffee_table, name='coffeetable'),
    path('Kingbed/',views.king_bed, name='kingbed'),
    path('LoungeChair/',views.lounge_chair, name='loungechair'),
    path('Moderndining/',views.modern_dining, name='moderndining'),
    path('product-detail/', views.ProductView.as_view(),name='productdetail'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='productdetail'),
    
    path('Seatings/',views.seatings, name='seatings'),
    path('Sofas/',views.sofa, name='sofa'),
    path('Swing/',views.swing, name='swing'),
    path('Storages/',views.storage, name='storage'),
    path('StudyTable/',views.study_table, name='studytable'),
    path('Tables/',views.table, name='table'),
    path('TVUnits/',views.tv_unit, name='tvunit'),
    path('WallCoverage/',views.wall_coverage, name='wallcoverage'),
    path('WallMount/',views.wall_mount, name='wallmount'),
    path('WoodenDining/',views.wooden_dining, name='woodendining'),
    path('address/', views.address, name='address'),
    path('checkout/', views.checkout, name='checkout'),
    # path('buynow/',views.buy_now, name='buynow'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)