import operator

from rest_framework import generics, status
from rest_framework.exceptions import ParseError

from crossfit.models import WorkOutRecord
from crossfit.serializers import RankSerializer


class Ranking(generics.ListAPIView):
    serializer_class = RankSerializer

    def get_queryset(self):
        workout = self.request.query_params.get('workout', None)
        if not WorkOutRecord.is_workout_in_choice(workout=workout):
            raise ParseError(detail='workout 형식이 올바르지 않습니다.', code=status.HTTP_400_BAD_REQUEST)
        return WorkOutRecord.get_rank(workout=workout)