from rest_framework import generics
from user.permissions import IsAdmin
from .models import Program, DailyStudy
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