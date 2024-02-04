from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# internals
from chatbot.serializers import CodeExplainSerializer
from chatbot.models import CodeExplainer


class CodeExplainView(views.APIView):
    serializer_class = CodeExplainSerializer
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        qs = CodeExplainer.objects.all()
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)