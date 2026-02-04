import datetime
from .receivers import read_signal
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from .serializers import CRUDSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
# naveenlars

# class RegisterAPIView(APIView):
#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         user = serializer.save()
#         return Response(data={
#             'message': 'user created successfully',
#             'user_id': user.id,
#             'email': user.email,
#         }, status=status.HTTP_201_CREATED)


# class RegisterAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegisterSerializer

#     def post(self, request):
#         return self.create(request)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        refresh_token = RefreshToken.for_user(user)
        return Response(data={
            'message': 'Login Successful',
            'access': str(refresh_token.access_token),
            'refresh_token': str(refresh_token),
            'user_id': user.id,
            'email': user.username

        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(data={
                'message': 'Logout successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'invalid or expired refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)


# class GetProfilesAPIView(APIView):
    # def get(self, request):
    #     users = User.objects.all()
    #     serializer = CRUDSerializer(users, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


# class ProfileAPI(APIView):
    # def get_user_object(self, pk):
    #     return get_object_or_404(User, id=pk)

    # def get(self, request, pk):
    #     user = self.get_user_object(pk=pk)
    #     serializer = CRUDSerializer(user)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def put(self, request, pk):
    #     serializer = CRUDSerializer(
    #         self.get_user_object(pk=pk), data=request.data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request, pk):
    #     user = self.get_user_object(pk=pk)
    #     user.delete()
    #     return Response(data='Deleted Successfully', status=status.HTTP_204_NO_CONTENT)

# class GenericProfilesAPI(GetProfilesAPIView,generics.ListAPIView):
    # queryset=User.objects.all()
    # serializer_class=CRUDSerializer
    # def get_queryset(self):
    #     return User.objects.filter(is_superuser=False)
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)


# class GenericProfileAPI(ProfileAPI,generics.RetrieveUpdateDestroyAPIView):
    # queryset=User.objects.all()
    # serializer_class=CRUDSerializer
    # lookup_field='pk'

    # def get(self,request,**kwargs):
    #     return self.retrieve(request,**kwargs)
    # def put(self,request,**kwargs):
    #     return self.update(request,**kwargs)
    # def delete(self,request, **kwargs):
    #     return self.destroy(request,**kwargs)

# class ProfilesAPIView(mixins.ListModelMixin,
#                       generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = CRUDSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# class ProfileAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = CRUDSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class Home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        date_time = datetime.datetime.now()
        read_signal.send(sender=request, date_time=date_time)
        return Response(data={
            'Home': 'Hello World'
        })














class UsersViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = CRUDSerializer
    # in modern development, get_serializer_class is standard way

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        return super().get_serializer_class()

    # Here, redefining create action to override the standard viewset create action
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Here, using action decorator to add custom actions to methods like [post,get] and it
    # will create a separate endpoint
    # @action(methods=['post'], detail=False, serializer_class=UserRegisterSerializer)
    # def register(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
