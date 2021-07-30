from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class AccountUrlList(APIView):
    """
    View to list all urls related to user accounts in the system.

    * Does not require token authentication.
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        """
        Return a list of all user account related urls.
        """
        api_urls = {
            "Urls": "account/",
            "Register": "account/register/",
            "Email Verification": "account/verify-email/",
            "Resend Email Verification": "account/resend-verification/",
            "Login": "account/login/",
            "Logout": "account/logout",
            "User Email List + Add": "account/emails/",
            "View, Delete Email": "account/emails/<pk>/",
            # "User": "account/user/",
            "Change Password": "account/password/change/",
            "Request Password Reset": "account/request-password-reset/",
            "Password Rest Confirmation": "account/reset-password/",
        }
        return Response(api_urls)
