from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProfileView, HomeView, AdminDashboardView, ProfileApprovalView #, approve_registration, reject_registration, admin_dashboard,

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('profile/<int:user_id>/<str:action>/', ProfileApprovalView.as_view(), name='profile_action'),
    # path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', HomeView.as_view(), name='home'),
    # path('admin/approve/<int:user_id>/', approve_registration, name='approve_registration'),
    # path('admin/reject/<int:user_id>/', reject_registration, name='reject_registration'),
]



# from django.urls import path
# from .views import RegisterView, LoginView, LogoutView, ProfileView, ApproveUsersView, HomeView

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('profile/', ProfileView.as_view(), name='profile'),
#     path('approve-users/', ApproveUsersView.as_view(), name='approve_users'),
    
#     path('home/', HomeView.as_view(), name='home'),
    
# ]








# urlpatterns = [
    
#     path("register/", register, name='register'),
#     path("login/", log_in, name='login'),
#     path('logout/', log_out, name='logout'),
#     path('profile/', profile, name='profile'),
#     path('home/', home, name='home'),
    
#     # dashboards
#     path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
#     path('instructor-dashboard/', instructor_dashboard, name='instructor_dashboard'),
#     path('student-dashboard/', student_dashboard, name='student_dashboard'),
# ]