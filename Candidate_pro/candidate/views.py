from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .serializers import CandidateSerializer
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import Candidate
from rest_framework.viewsets import ModelViewSet
from .paginations import CandidateViewPagination
from .producer import publish


class CandidateListView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()
    pagination_class = CandidateViewPagination

    def get(self, request):
        return self.list(request)

    def get_permissions(self):
        """
            Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        city_name = self.request.query_params.get('city_name', None)
        tech_skills = self.request.query_params.get('tech_skills', None)
        # list_tech_skills = tech_skills.split(",") if tech_skills else []
        qs = self.queryset
        if city_name:
            qs = qs.filter(city_name__exact=city_name)
        if tech_skills:
            qs = qs.filter(tech_skills__contains=tech_skills)

        return qs.order_by('id')

    def post(self, request, bulk=None):
        candidate_data = JSONParser().parse(request)
        if bulk:
            print("Bulk input")
            candidate_serializer = CandidateSerializer(data=candidate_data, many=True)
        else:
            print("No bulk")
            candidate_serializer = CandidateSerializer(data=candidate_data)

        if candidate_serializer.is_valid():
            candidate_serializer.save()
            c_data = candidate_serializer.data
            if not bulk:
                c_data['tech_skills'] = list(c_data['tech_skills'])
                publish('candidate_created', c_data)
            return Response(candidate_serializer.data, status=status.HTTP_201_CREATED)
        return Response(candidate_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
