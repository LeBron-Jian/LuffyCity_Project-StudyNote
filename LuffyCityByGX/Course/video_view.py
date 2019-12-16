# by gaoxin
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.polyv import polyv_video


class PolyvView(APIView):
    def post(self, request):
        # 向保利威视频发送请求获取token能够播放加密视频
        vid = request.data.get("vid", "")
        ip = request.META.get("REMOTE_ADDR", "")
        # 根据业务逻辑获取用户的id以及username
        uid = "123",
        username = "gaoxin"
        print(vid, ip)
        data = polyv_video.get_verify_data(vid, ip, uid, username)
        print(data)
        return Response(data["token"])