from django.urls import path
from app import views
from app.middlewares import firstmiddleware
from app.middlewares import secondmiddleware

urlpatterns = [
    path("login/",views.login,name="login"),
    path("logout/",views.logout,name="logout"),
    path("project/",firstmiddleware(views.project),name="project"),
    path("dashboard/",firstmiddleware(views.dashboard),name="dashboard"),
    path("success/",firstmiddleware(views.success),name="success"),
    path('delete/<int:project_id>/', views.delete, name='delete'), 
    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path("round1/<int:project_id>/",secondmiddleware(views.round1),name="round1"),
    path("round2/<int:project_id>/",secondmiddleware(views.round2),name="round2"),
    path("round3/<int:project_id>/",secondmiddleware(views.round3),name="round3"),
]