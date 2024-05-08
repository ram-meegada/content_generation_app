from whizzo_app.services.uploadMediaService import UploadMediaService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
upload_media_obj = UploadMediaService()

class UploadMediaView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        result = upload_media_obj.upload_media(request)
        return Response(result, status=result["status"])