from rest_framework.views import APIView
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from rest_framework.response import Response
from rest_framework import status


class InvoiceView(APIView):
    def get_data(self, id):
        return {'invoice_customer_name': '', 'item_details': [{}, {}, {}]}
    def post(self, request):
        data = request.data
        # Invoice serializer creation
        serializer_invoice = InvoiceSerializer(data=data)
        if serializer_invoice.is_valid():
            inv_obj = serializer_invoice.save()
        else:
            return Response({'msg': 'Not valid'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        for item in data['item_details']:
            item['invoice'] = inv_obj.id

        inv_detail_serializer = InvoiceDetailSerializer(data=data['item_details'], many=True)
        if inv_detail_serializer.is_valid():
            inv_detail_obj = serializer_invoice.save()
            return Response({'data': self.get_data(inv_obj.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'Not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExists:
            return Response({'msg': 'Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': self.get_data(invoice.id)}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        pass

    def delete(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExists:
            return Response({'msg': 'Not Found'}, status=status.HTTP_400_BAD_REQUEST)

        invoice.delete()
        return Response({'msg': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)





