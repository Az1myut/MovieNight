from django.shortcuts import redirect
import requests
from rest_framework_simplejwt.tokens import OutstandingToken
from django.utils.deprecation import MiddlewareMixin
import jwt
from jwt.exceptions import ExpiredSignatureError
from django.conf import settings
from icecream import ic
from django.contrib.auth import logout


class AccessTokenCheckMiddleware(MiddlewareMixin):
    def is_token_valid(self, token):
        if token:
            try:
                payload = jwt.decode(
                    jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
                return True
            except ExpiredSignatureError:
                return False
        return False

    def process_response(self, request, response):
        allowed_pathes = ['/registration/login/',
                          '/registration/register/',
                          '/registration/logout/']

        if request.path in allowed_pathes:

            return response

        user = request.user
        if user.is_authenticated:
            access_token = request.COOKIES.get('access_token')

            is_access_token_valid = self.is_token_valid(access_token)
            if is_access_token_valid:

                return response
            else:
                outstanding_token = OutstandingToken.objects.filter(
                    user=request.user).first()

                refresh_token = outstanding_token.token
                is_refresh_token_valid = self.is_token_valid(refresh_token)
                if is_refresh_token_valid:

                    resp = requests.post('http://127.0.0.1:8000/api/token/refresh/', data={
                        'refresh': refresh_token})

                    result = resp.json()
                    new_access_token = result.get('access')
                    response.set_cookie('access_token', new_access_token)
                    return response

                else:

                    outstanding_token.delete()
                    logout(request=request)
                    return redirect('registration:login')
        return response
