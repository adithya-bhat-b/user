from json import load
from os import path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from user_activity.models import User, UserActivity

class Command(BaseCommand):
    help = 'Stores the user and user activity in db'

    # def add_arguments(self, parser):
    #     parser.add_argument('--json_file', nargs='+', type=str)

    def handle(self, *args, **options):
        file_path = path.join(settings.BASE_DIR, "static/data/db_data.json")
        if path.exists(file_path):
            with open(file_path) as fp:
                db_data = load(fp)
            for user_info in db_data:
                user_name = user_info.get("real_name")
                user = User(
                    id=user_info.get("id"),
                    real_name=user_name,
                    time_zone=user_info.get("tz")
                )
                try:
                    user.full_clean()
                except Exception as err:
                    self.stderr.write("Error creating user: %s, Error: %s" % 
                                    (user_name, err))
                else:
                    user.save()
                    self.stdout.write("User: %s is stored successfully" % user_name)
                    for activity in user_info.get("activity_periods", []):
                        user_activity = UserActivity(
                            user_id=user,
                            start_time=activity.get("start_time"),
                            end_time=activity.get("end_time")
                        )
                        try:
                            user_activity.full_clean()
                        except Exception as err:
                            self.stderr.write("Error creating user-activity for: %s, "
                                            "Error: %s" % (user_name, err))
                        else:
                            user_activity.save()
        else:
            self.stderr.write("Json file:%s to populate db data doesn't exist" 
                              % file_path)