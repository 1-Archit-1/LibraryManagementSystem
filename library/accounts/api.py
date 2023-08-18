from rest_framework import generics
from rest_framework.response import Response
from .permissions import LibPermission
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from .serializer import LibRegisterSerializer,MemRegisterSerializer, UserSerializer,MemViewSerializer


from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class LibRegisterApi(generics.GenericAPIView):
    serializer_class = LibRegisterSerializer
    def post(self, request, *args,  **kwargs):
        """Register a  Libriarian account"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
class MemRegisterApi(generics.GenericAPIView):
    serializer_class = MemRegisterSerializer
    def post(self, request, *args,  **kwargs):
        """Register a  Member account"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class AddMember(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, LibPermission,)
    serializer_class = MemRegisterSerializer
    def post(self, request, *args,  **kwargs):
        """Allows librarians to add new members"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        return Response({
            "member": MemRegisterSerializer(member).data,
            "message": "Member added Successfully",
        })

class Viewmembers(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, LibPermission,)
    @extend_schema(parameters=[OpenApiParameter(name='pk',description='id of user to view , not needed if viewing all members'),])
    def get(self,request):
        """View members """
        try:

            if request.query_params:
                members = CustomUser.objects.get(id =request.query_params.get('pk') )
                if members:
                    member =MemViewSerializer(members)
            else:
                members = CustomUser.objects.all()
                if members:
                    member = MemViewSerializer(members , many =True)

            if members:
                return Response({
                    "member": member.data,
                })
        except Exception as e:
            return Response("user not found")

class RemoveMembers(generics.GenericAPIView):
    @extend_schema(parameters=[OpenApiParameter(name='pk',description='id of user to remove , not needed if deleting own account',)])
    def delete(self, request):
        """Remove own account or allows librarians to remove other members account"""
        try:
            if request.query_params.get('pk') is not None:
                member_to_delete =  CustomUser.objects.get(id=request.query_params.get('pk'))
            else:
                member_to_delete =  CustomUser.objects.get(id=request.user.id)
                member_to_delete.delete()
                return Response({
                    'message': 'Member Deleted Successfully'
                })

            if member_to_delete.user_type == 1 and member_to_delete.id!= request.user.id:
                return Response({
                    'message': 'cannot delete librarian account'
                })
            if request.user.user_type == 1 or (request.user.user_type == 2 and member_to_delete.id == request.user.id):
                member_to_delete.delete()
                return Response({
                    'message': 'Member Deleted Successfully'
                })
            else:
                return Response({
                    'message': 'Cannot delete other accounts'
                })

        except Exception as e:
            print(e)
            return Response({'error':'not found'})

class UpdateMember(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, LibPermission,)
    @extend_schema(
        request = MemViewSerializer,
        parameters=[
            OpenApiParameter(
                name='pk',
                description = 'id of the member to update'),])
    def put(self, request,):
        """Update a member account"""
        try:
            member = CustomUser.objects.get(id =request.query_params.get('pk') )
            if member.user_type == 1:
                return Response({
                    'message': 'cannot update librarian account'
                })
            serializer = MemViewSerializer(instance=member,data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'message': 'Action completed successfully',
                'data': serializer.data
            })
        except Exception as e:
            print(e)
            return Response('error')