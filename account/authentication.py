from account.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user: User = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None
