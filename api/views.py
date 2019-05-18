from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import User, Transfer
from .serializers import UserSerializer, TransferSerializer


class UserView(APIView):
    permission_classes = (AllowAny, )

    # CREATES A USER, IT ALSO CREATES A WALLET ALONG WITH IT IN THE SERIALIZER
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(request.data)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors, 'message': 'BAD REQUEST: Could not create user'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id, format=None):
        # ONLY ALLOW TO CHECK OWN DETAILS
        if request.user and id == request.user.id:
            user = UserSerializer(User.objects.get(id=id))
            return Response(user.data, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_403_FORBIDDEN)


class TransferView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, id, format=None):
        if request.user and id == request.user.id:
            transfer = {
                'from_user': request.user.id,
                'to_user': int(request.data.get('to_user')),
                'amount': request.data.get('amount')
            }
            serializer = TransferSerializer(transfer)
            if serializer.is_valid and transfer['from_user'] != transfer['to_user']:
                transfer = Transfer.create(**transfer)
                return Response(UserSerializer(User.objects.get(id=id)).data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Malformed request', 'message': 'You cannot transfer balance to yourself'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({}, status=status.HTTP_403_FORBIDDEN)
