import uuid
from django.utils.deprecation import MiddlewareMixin

class GuestSessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated and 'session_id' not in request.session:
            request.session['session_id'] = uuid.uuid4().hex