from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework.response import Response
from rest_framework import status, generics
from django.db import connection


logger = logging.getLogger(__name__)
cursor = connection.cursor()


# Create your views here.
class GetVolume(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        try:
            request_data = request.data
            driver_top_level = request_data['driver_top_level']
            driver_sub_level_1 = request_data['driver_sub_level_1']
            driver_sub_level_2 = request_data['driver_sub_level_2']
            value = request_data['value']

            cursor.execute('''SELECT value FROM db_volume WHERE driver_type=%s and driver_name=%s and type=%s''',
                           [driver_top_level, driver_sub_level_1, driver_sub_level_2])
            row = cursor.fetchall()
            value = row[0][0]

            response = {}
            response['message'] = f"Volume for {driver_top_level}>{driver_sub_level_1}>{driver_sub_level_2}"
            response['volume'] = value
            return Response(response, status=status.HTTP_200_OK)

        except Exception as error:
            logger.exception(error)
            response = {
                'message': "Request data not valid"
            }
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
