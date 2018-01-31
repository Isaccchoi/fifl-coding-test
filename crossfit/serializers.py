from rest_framework import serializers

from .models import WorkOutRecord


class RankSerializer(serializers.ModelSerializer):
    center = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = WorkOutRecord
        fields = (
            'rank',
            'record_time',
            'user_id',
            'center',
        )

    def get_center(self, obj):
        return obj.user.crossfit_center.name

    def get_user_id(self, obj):
        return obj.user.user_id

    def get_rank(self, obj):
        return obj.rank