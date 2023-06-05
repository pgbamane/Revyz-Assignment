from rest_framework import mixins
from rest_framework import generics
from .serializers import CandidateSerializer
from .models import Candidate


# Create your views here.
class CandidateListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = CandidateSerializer
    queryset = Candidate.objects.all()

    def get(self, request):
        return self.list(request)

    def get_queryset(self):
        qs = self.queryset
        return qs.order_by('id')
