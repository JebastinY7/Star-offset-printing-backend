from django.utils.timezone import now
from .models import StaffActivity

class StaffLastSeenMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            activity, created = StaffActivity.objects.get_or_create(
                user=request.user
            )

            activity.last_seen = now()
            activity.save(update_fields=['last_seen'])

        return self.get_response(request)