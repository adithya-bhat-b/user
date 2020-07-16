import json
import logging

from django.http import HttpResponse
from django.shortcuts import render

from user_activity.models import User, UserActivity

logger = logging.getLogger(__name__)
# Create your views here.

def get_users(request): 
    """
    This function is used to get all the users and their activities
    from the database
    """
    invalid_http_method_err = "Invalid http method, use get"
    if request.method == "GET":
        users = User.objects.all()
        all_users = []
        for user in users:
            all_users.append(_get_user_json(user))
        ret_json = {
            "ok": True,
            "members": all_users
        }
        logger.info("Users are retrieved successfully")
        logger.debug("Users with their activities: %s" % ret_json)
        return HttpResponse(json.dumps(ret_json))
    return HttpResponse(invalid_http_method_err)

def _get_user_json(user):
    """
    Function to create result user json from user object
    """
    date_format_str = "%b %d %Y %I:%M%p"
    user_activities = []
    for activity in user.useractivity_set.values():
        activity_json = {
            "start_time": activity["start_time"].strftime(date_format_str),
            "end_time": activity["end_time"].strftime(date_format_str)
        }
        user_activities.append(activity_json)
    user_json = {
        "id": user.id,
        "real_name": user.real_name,
        "tz": user.time_zone,
        "activity_periods": user_activities
    }
    logger.debug("Activity for the user: %s is: %s." % (user.id, user_activities))
    return user_json