from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import *
from .serializers import (
    PerevalSerializer, UserSerializer, CoordsSerializer, LevelSerializer, ImagesSerializer
)


def reverse_to_submit(request):
    return redirect('submitData')


class PerevalAPIViewSet(viewsets.ViewSet):
    @staticmethod
    def response_serializer_error(errors, param='id'):
        message = ''
        for k, v in errors.items():
            message += f'{k}: {str(*v)}'

        if param == 'state':
            return Response({'message': message, 'state': 0}, status=400)
        else:
            return Response({'message': message, 'id': None}, status=400)

    def add_dependence(self, serializer):
        if serializer.is_valid():
            return serializer.save()
        else:
            return self.response_serializer_error(serializer.errors)

    @api_view(['POST'])
    def post(self, request):
        try:
            data = request.data
            if not data:
                return Response({'message': 'Empty request', 'id': None}, status=400)

            try:
                user = User.objects.get(email=data['user']['email'])
                user_serializer = UserSerializer(user, data=data['user'])
            except:
                user_serializer = UserSerializer(data=data['user'])

            try:
                images = data['images']
                data.pop('images')
            except:
                images = []

            main_serializer = PerevalSerializer(data=data)
            if main_serializer.is_valid():
                try:
                    data.pop('user')
                    new_pereval = Pereval.objects.create(
                        user=self.add_dependence(user_serializer),
                        coords=self.add_dependence(CoordsSerializer(data=data.pop('coordinates'))),
                        levels=self.add_dependence(LevelSerializer(data=data.pop('levels'))),
                        **data
                    )
                except Exception as e:
                    return Response({'message': str(e), 'id': None}, status=400)
            else:
                return self.response_serializer_error(main_serializer.errors)

            for i in images:
                i['pereval_id'] = new_pereval.id
                self.add_dependence(ImagesSerializer(data=i))

            return Response({'message': 'Success', 'id': new_pereval.id}, status=201)

        except Exception as e:
            return Response({'message': str(e), 'id': None}, status=500)

    def get_pereval(self, request, **kwargs):
        try:
            pereval = Pereval.objects.get(pk=kwargs['pk'])
            data = PerevalSerializer(pereval).data
            return Response(data, status=200)
        except:
            return Response({'message': 'Such a record does not exist', 'id': None}, status=404)

    def edit_pereval(self, request, **kwargs):
        try:
            pereval = Pereval.objects.get(pk=kwargs['pk'])
            if pereval.status == 'new':
                data = request.data
                data.pop('user')
                images = data.pop('images')
                serializers = [CoordsSerializer(Coords.objects.get(id=pereval.coordinates),
                                                data=data.pop('coordinates')),
                               LevelSerializer(Level.objects.get(id=pereval.levels),
                                               data=data.pop('levels')),
                               PerevalSerializer(pereval, data=data)]
                Images.objects.filter(pereval_id=pereval.id).delete()
                for i in images:
                    i['pereval_id'] = pereval.id
                    serializers.append(ImagesSerializer(data=i))
                for s in serializers:
                    if s.is_valid():
                        s.save()
                    else:
                        return self.response_serializer_error(s.errors, 'state')
                return Response({'message': 'Success', 'state': 1}, status=200)
            else:
                return Response({'message': "Status is not 'new'", 'state': 0}, status=400)
        except:
            return Response({'message': 'Such a record does not exist', 'id': None}, status=404)

    def get_user_perevals(self, request, **kwargs):
        try:
            user = User.objects.get(email=request.GET['user__email'])
            perevals = Pereval.objects.filter(user=user)
            data = PerevalSerializer(perevals, many=True).data
            return Response(data, status=200)
        except:
            return Response({'message': 'Records not found'}, status=200)
