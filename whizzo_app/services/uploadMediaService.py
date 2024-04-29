from whizzo_app.models.uploadMediaModel import UploadMediaModel
from whizzo_app.utils.saveImage import save_image
from whizzo_app.serializers.uploadMediaSerializer import CreateUpdateUploadMediaSerializer
from whizzo_app.utils import messages

class UploadMediaService:
    def upload_media(self, request):
        images = dict(request.data)["media"]
        try:
            response_data = []
            for img in images:
                image_response = save_image(img)
                data = {
                    "media_url": image_response[0],
                    "media_type": img.content_type,
                    "media_size": img.size,
                    "media_name": img.name
                }
                serializer = CreateUpdateUploadMediaSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                response_data.append(serializer.data)    
            return {"data": response_data, "message": messages.MEDIA_UPLOADED, "status": 200}
        except:        
            return {"data": serializer.errors, "message": messages.WENT_WRONG, "status": 400}