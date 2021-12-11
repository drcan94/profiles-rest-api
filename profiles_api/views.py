from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


from .serializers import HelloSerializer, UserProfileSerializer, ProfileFeedItemSerializer
from .models import UserProfile, ProfileFeedItem
from .permissions import UpdateOwnProfile, UpdateOwnStatus

class HelloApiView(APIView):
    """ Test APIView """

    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """ Returns a list of APIView features """
        an_apiview = [
            'Uses HTTP methods as function (get,post,patch,put,delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over application logic',
            'Is mapped manually to URLs'
        ]
        return Response({'message' : 'Hello!','an_apiview' : an_apiview})

    def post(self, request):
        """ Create a hello message with our name """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status = HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk=None):
        """ Handle updating an object """
        return Response({'method' : 'PUT'})

    def patch(self, request, pk=None):
        """ Handle a partial updating an object """
        return Response({'method' : 'PATCH'})

    def delete(self,request,pk=None):
        """ Delete an Object """
        return Response({'method' : "DELETE"})


class HelloViewSet(ViewSet):
    """ Test ViewSet """

    serializer_class = HelloSerializer

    def list(self, request):
        """ Return a hello message """
        a_viewset = [
            "Uses actions (List, create, retrieve, update, partial_update, destroy)",
            "Automatically maps to URLs using Routers",
            "Provides more functionality with less code",
        ]
        return Response({
            'message' : 'Hello!',
            'a_viewset' : a_viewset
        })

    def create(self, request):
        """ Create a new hello message """

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get("name")
            message = f'Hello {name}!'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )
    def retrieve(self, request, pk=None):
        """ Handle getting an object by its id """
        return Response({"http_method" : 'GET'})

    def update(self, request, pk=None):
        """ Handle updating an object """
        return Response({'http_method' : 'PUT'})

    def partial_update(self, request, pk=None):
        """ Handle a partial updating an object """
        return Response({'http_method' : 'PATCH'})

    def destroy(self, request, pk=None):
        """ Delete an Object """
        return Response({'http_method' : 'DELETE'})


class UserProfileViewSet(ModelViewSet):
    """ Handle creating and updating profiles """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    authentication_classes = (TokenAuthentication,)
    # yetkilendirme yöntemini token ile olsun şeklinde belirledik
    permission_classes = (UpdateOwnProfile,)

    filter_backends = (SearchFilter,)
    search_fields = ('name','email',)


class UserLoginAPIView(ObtainAuthToken):
    """ Handle creating user authentication tokens """

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ProfileFeedItemViewSet(ModelViewSet):
    """ Handles creating, reading and updating profile feed items """

    authentication_classes = (TokenAuthentication,)
    serializer_class = ProfileFeedItemSerializer
    queryset = ProfileFeedItem.objects.all()
    permission_classes = (
        UpdateOwnStatus,
        # IsAuthenticatedOrReadOnly
        IsAuthenticated
    )

    def perform_create(self, serializer):
        """ Sets the user profile to the logged in user """

        serializer.save(user_profile = self.request.user)
