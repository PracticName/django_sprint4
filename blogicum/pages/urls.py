from django.urls import path
# from . views import AboutTemplateView, RulesTemplateView
from django.views.generic import TemplateView

app_name = 'pages'

urlpatterns = [
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('rules/', TemplateView.as_view(template_name='pages/rules.html'), name='rules'),
]
