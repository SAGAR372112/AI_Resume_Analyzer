from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobDescriptionSerializer, ResumeSerializer
from .models import JobDescription, Resume
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ResumeSerializer
import traceback
from .analyzer import process_resume


class JobDescriptionAPIView(APIView):
    def get(self, request):
        try:
            job_descriptions = JobDescription.objects.all()
            serializer = JobDescriptionSerializer(job_descriptions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AnalyzeResumeAPI(APIView):
    def post(self, request):
        try:
            print("Start analyzing resume...")
            data = request.data
            print("Incoming data:", data)

            # Check required fields
            if 'job_description' not in data:
                return Response({
                    'status': False,
                    'message': 'Job description is required.',
                    'data': {}
                })
            
            if 'resume' not in request.FILES:
                return Response({
                    'status': False,
                    'message': 'Resume file is required.',
                    'data': {}
                })

            # Prepare data for serializer
            serializer = ResumeSerializer(data={
                'resume': request.FILES['resume'],
                'job_description': data.get('job_description')
            })

            if not serializer.is_valid():
                print("Serializer errors:", serializer.errors)
                return Response({
                    'status': False,
                    'message': 'Validation failed.',
                    'data': serializer.errors
                })

            instance = serializer.save()
            print("Data saved successfully:", instance.id)
            print("Resume path:", instance.resume.path)
            _data = serializer.data
            resume_instance = Resume.objects.get(id = _data['id'])
            resume_path = resume_instance.resume.path
            data = process_resume(resume_path, JobDescription.objects.get(id=data.get('job_description')).job_description)

            # You can add your analysis logic here later
            return Response({
                'status': True,
                'message': data,
                'data': serializer.data
            })

        except Exception as e:
            print("Error occurred:", str(e))
            traceback.print_exc()
            return Response({
                'status': False,
                'message': str(e),
                'data': {}
            })
