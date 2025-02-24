from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import dashboad
from django.conf.urls import handler404
from .views import submit_amo_form,AmoListView,AmoMipangokaziListView,AmoTaarifaListView,RegistrationView,MipangokaziHazinaCreateView, ReceiptsPerIndividualViewSet,UserProfileView, BankCashReconciliationViewSet, CashBudgetRecordsViewSet,AssetListAPIView

handler404 = 'accounts.views.page_not_found'


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('auth/login-page/',views.Logged_in,name='Logged_in'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('Iyumbu-user/dashboad/', views.dashboad, name='dashboad'),
    path('user/user-api/help', views.help_view, name='help'),
    path('pages/add-page/pages_register', views.pages_register, name='pages_register'),
    path('users/useer-profile',  views.user_profile, name='user_profile'),
    path('iyumbu-members/washiriki-api/wote', views.washiriki_view, name='washiriki'),
    path('matoleo/graph/barchart/view-api', views.chart_view, name='chart'),
    path('elders/api-view-inf/',views.wazee_view_info,name='wazee_view'),
    path('cashier/api-view-inf', views.mhazini_view_info,name='cashier'),
    path('secretary/api-secretary-view/inf/',views.karani_view_info,name='karani_inf'),
    path('deacons/iyumbu/apk-view/',views.mashemasi_view_info,name='mashemasi_view_info'),
    path('youth/adventist-youth/api-view/inf/',views.vijana_view_info,name='vijana_view_info'),
    path('shule-sabato/api-view/inf/',views.sabato_view_info,name='sabato_view_info'),
    path('ujenzi/build/inf-api/',views.kwaya_view_info,name='kwaya_view_info'),
    path('ladies/dorcas-api/inf/',views.dorasc_view_info,name='dorasc_view_info'),
    path('miradi/api-view/inf/',views.miradi_view_info,name='miradi_view_info'),
    path('huduma/api/view-inf/inf/',views.huduma_view_info,name='huduma_view_info'),
    path('matukio/ratiba/api-inf/view/',views.karendar_view_info,name='karendar_view_info'),
    path('matoleo/view/inf/api/',views.matoleo_fill_info,name='matoleo_fill_info'),
    # page error
    path('pages/error/', views.page_not_found, name='page_not_found'),
    
    # Password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('continue/', views.continue_view, name='continue'), 
    path('users/base/auth/',views.base_view,name='base'),
   

    # #########################################FORMS####################################3333
   path('forms/elders/', views.wazee_view, name='wazee'),
   path('forms/mhazini/', views.mhazini_view, name='mhazini'),
   path('forms/karani/', views.karani_view, name='karani'),
   path('forms/mashemasi/', views.mashemasi_view, name='mashemasi'),
   path('forms/shule-sabato/', views.shule_view, name='shule'),
   path('forms/ujenzi/', views.ujenzi_view, name='ujenzi'),
   path('forms/vijana/', views.vijana_view, name='vijana'),
   path('forms/amo-ap/', views.kwaya_view, name='kwaya'),
   path('forms/dorkasi/', views.dorcas_view, name='dorkasi'),
   path('forms/miradi-api/', views.wazee_view, name='miradi'),
   path('forms/kalendar-api/', views.kalendar_view, name='karenda'),
   path('forms/huduma-api/',views.huduma_view, name='huduma'),
   path('forms/amo-forms-api/',views.amo_view,name='amo'),
   path('',views.sign_up_view,name='sign-up'),
   path('contributions/api-form/', views.matoleo_view,name='matoleo'),


#    handling model requests
   path('api/request/', views.RequestCreateView.as_view(), name='api_request_create'),
   path('api/submit-amo-form/', submit_amo_form, name='submit_amo_form'),

#    APIs of rendering pages from the database
   path('api/amo-api/get-all-amo/', views.Amo_get,name='Amo_get'),

# APs for getting data from the databaseI
   path('api/get-all-amo/', AmoListView.as_view(), name='get-amo-forms'),
   path('api/amo/mipangokazi/', AmoMipangokaziListView.as_view(), name='amo-mipangokazi-list'),
   path('api/amo/taarifa/', AmoTaarifaListView.as_view(), name='amo-taarifa-list'),
   path('api/registrations/', RegistrationView.as_view(), name='registration-list'),
   path('api/mipangokazi/', MipangokaziHazinaCreateView.as_view(), name='mipangokazi-create'),
   

    
   # ReceiptsPerIndividual API
   path('api/receipts/', ReceiptsPerIndividualViewSet.as_view({'get': 'list', 'post': 'create'}), name='receipts-list'),
    
    # BankCashReconciliation API
   path('api/banks-reconciliation/', BankCashReconciliationViewSet.as_view({'get': 'list', 'post': 'create'}), name='banks-reconciliation-list'),
    
    # CashBudgetRecords API
   path('api/cash-budget/', CashBudgetRecordsViewSet.as_view({'get': 'list', 'post': 'create'}), name='cash-budget-list'),
   path('Tithes/add-tithe/', views.add_tithe, name='add_tithe'),
   # view info by token
   path('api/tithes/info-/', views.get_user_tithes, name='get_user_tithes'),


   # elders
    path('api/create_user_info/', views.create_user_info, name='create_user_info'),
    path('create_cv/', views.create_cv, name='create_cv'),
    path('create_work_plan/', views.create_work_plan, name='create_work_plan'),
    path('create_feedback/', views.create_feedback, name='create_feedback'),
    path('get_all_data/', views.get_all_data, name='get_all_data'), 
    path('api/assets/', AssetListAPIView.as_view(), name='asset-list'),
    path('api/userprofile/', UserProfileView.as_view(), name='userprofile-api'), 
   # user profile


]

