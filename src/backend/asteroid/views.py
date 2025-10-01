from rest_framework.views import APIView

from asteroid.models import Asteroid
from asteroid.serializers import BriefAsteroidSerializer


class AsteroidListView(APIView):
    queryset = Asteroid.objects.all()
    serializers = BriefAsteroidSerializer
