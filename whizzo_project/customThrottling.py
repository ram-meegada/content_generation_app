from rest_framework.throttling import AnonRateThrottle
from rest_framework.response import Response
from rest_framework import status

class CustomAnonRateThrottle(AnonRateThrottle):
    def throttle_failure(self):
        """
        Return a custom response when a request is throttled.
        """
        return Response(
            {
                'detail': 'You have made too many requests. Please try again later.'
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
