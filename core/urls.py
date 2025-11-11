from django.contrib import admin
from django.urls import path
from resume_analyzer.views import AnalyzeResumeAPI, JobDescriptionAPIView, TestAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/job-descriptions/', JobDescriptionAPIView.as_view(), name='job-descriptions'),
    path('api/v1/resume-analyze/', AnalyzeResumeAPI.as_view(), name='analyze-resume'),
    path('api/v1/test/', TestAPI.as_view(), name='test'),
]
