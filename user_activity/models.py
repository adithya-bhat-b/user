import pytz
from django.db import models

# Create your models here.

def _get_time_zones():
    """
    Function to get all the timezones
    """
    timezone_choices = [(tz, tz) for tz in pytz.all_timezones]
    return timezone_choices

#  Model for user
class User(models.Model):
    """
    User model:
        attributes:
            id - unique id of the user
            real_name - user name
            time_zone - user timezone
    """
    id = models.CharField(primary_key=True, max_length=50)
    real_name = models.CharField(max_length=100)
    time_zone = models.CharField(max_length=50, choices=_get_time_zones())

    class Meta:
        # Db table name
        db_table = "user"

#  Model for user
class UserActivity(models.Model):
    """
    UserActivity model:
        start_time: start time of an user activity
        end_time: end time of an user activity
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        # Db table name
        db_table = "user_activity"