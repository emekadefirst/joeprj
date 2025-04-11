from .models import Device
from rest_framework import generics
from user.permissions import IsAdmin
from .models import Program, DailyStudy
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from .serializers import ProgramSerializer, DailyStudySerializer



class ProgramView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [AllowAny()]
    

class ProgramRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [AllowAny()]
    


class DailyStudyView(generics.ListCreateAPIView):
    queryset = DailyStudy.objects.all()
    serializer_class = DailyStudySerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [AllowAny()]

class DailyStudyRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyStudy.objects.all()
    serializer_class = DailyStudySerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [AllowAny()]
    


@api_view(['POST'])
def register_device(request):
    token = request.data.get('token')
    platform = request.data.get('platform', 'android')
    user = request.user if request.user.is_authenticated else None  

    if token:
        device, created = Device.objects.get_or_create(token=token, defaults={
            'platform': platform,
            'user': user
        })
        
        if not created and device.user != user:
            device.user = user 
            device.save()
        return Response({"message": "Device registered."})
    return Response({"error": "Token required"}, status=400)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_push_notification

@api_view(['POST'])
def test_notification(request):
    try:
        title = request.data.get('title', 'Test Notification')
        body = request.data.get('body', 'This is a test message')
        
        result = send_push_notification(title, body)
        
        if result is None:
            return Response({
                'status': 'error',
                'message': 'Firebase not initialized or no valid devices'
            }, status=400)
            
        return Response({
            'status': 'success',
            'total_devices': result['total'],
            'success_count': result['success'],
            'results': result['results']
        })
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=500)