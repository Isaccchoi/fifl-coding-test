import operator

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(regex=r'^0([0-9]{1,2})-?([0-9]{3,4})-?([0-9]{4})$',
                             message="전화번호는 '010-1234-5678','01012345678','02-1234-5678', '0212345678' 형식으로 입력하여야 합니다.")

CHOICE_WORKOUT = (
    ('BARBARA', '바바라'),
    ('CHELSEA', '첼시'),
    ('CINDY', '신디'),
)


class Center(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=13)

    def __str__(self):
        return self.name


class WorkOutRecord(models.Model):
    user = models.ForeignKey('member.User', on_delete=models.CASCADE)
    workout_name = models.CharField(choices=CHOICE_WORKOUT, max_length=100)
    record_time = models.TimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    rank = int()

    def __str__(self):
        return f'{self.user.user_id} - {self.workout_name} - {self.record_time}'

    class Meta:
        ordering = ['workout_name', '-record_time']

    @classmethod
    def is_workout_in_choice(cls, workout):
        if workout not in dict(CHOICE_WORKOUT).keys():
            return False
        return True

    @classmethod
    def get_rank(cls, workout):
        record = cls.objects.filter(workout_name=workout).order_by('user_id', 'record_time')

        new_record = list(record)
        for i, rec in enumerate(new_record):
            if i != 0:
                if rec.user_id == new_record[i - 1].user_id:
                    del new_record[i]

        sorted_result = sorted(new_record, key=operator.attrgetter('record_time'))

        for i, rec in enumerate(sorted_result):
            if rec.record_time == sorted_result[i - 1].record_time:
                rec.rank = sorted_result[i - 1].rank
                continue
            rec.rank = i + 1

        return sorted_result
