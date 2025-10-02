from asteroid.models import Asteroid
from asteroid.serializers import BriefAsteroidSerializer
from rest_framework.views import APIView


class AsteroidListView(APIView):
    queryset = Asteroid.objects.all()
    serializers = BriefAsteroidSerializer
