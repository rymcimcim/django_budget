from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.tokens import AccessToken


def get_user_id_from_access_token(request):
    access_token_str = request.META.get('HTTP_AUTHORIZATION')
    access_token_obj = AccessToken(access_token_str.replace('Bearer ', ''))
    return access_token_obj['user_id']