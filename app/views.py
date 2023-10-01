from rest_framework.views import APIView
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer, InvoicedetailSerializer
from rest_framework.response import Response
from rest_framework import status


class InvoiceView(APIView):

    def get_data(self, key):
        inv_obj = Invoice.objects.get(id=key)
        inv_serializer = InvoiceSerializer(instance=inv_obj)
        inv_obj_data = dict(inv_serializer.data)
        invoice_detail_objects = list(InvoiceDetail.objects.filter(invoice=inv_obj.id))
        temp1 = []
        for i in range(len(invoice_detail_objects)):
            ele = invoice_detail_objects[i]

            if ele.quantity == 0:
                invoice_detail_objects[i] = None
                ele.delete()
            else:
                temp1.append(ele)

        invoice_detail_objects = temp1
        inv_detail_serializer = InvoicedetailSerializer(instance=invoice_detail_objects, many=True)
        inv_detail_dict_list = [dict(item) for item in inv_detail_serializer.data]
        inv_obj_data['item_details'] = inv_detail_dict_list
        return inv_obj_data

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
            inv_detail_serializer.save()
            return Response({'data': self.get_data(inv_obj.id)}, status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'Not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            return Response({'msg': 'Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'data': self.get_data(invoice.id)}, status=status.HTTP_200_OK)

    def put(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            return Response({'msg': 'Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer_invoice = InvoiceSerializer(instance=invoice, data=data, partial=True)

        if serializer_invoice.is_valid():
            serializer_invoice.save()
        else:
            return Response({'msg': 'Not valid'}, status=status.HTTP_400_BAD_REQUEST)

        old_invoice_obj = InvoiceDetail.objects.filter(invoice=pk)
        old_invoice_items = old_invoice_obj.values_list('description', flat=True)
        new_items = [item for item in data['item_details'] if item['description'] not in old_invoice_items]

        old_items = {item.description: item for item in old_invoice_obj}
        for item in data['item_details']:
            if item['description'] in old_items:
                inv_detail_serializer = InvoiceDetailSerializer(instance=old_items[item['description']], data=item,
                                                                partial=True)
                if inv_detail_serializer.is_valid():
                    inv_detail_serializer.save()
                else:
                    return Response({'msg': f'Not valid details for {item}'}, status=status.HTTP_400_BAD_REQUEST)

        if len(new_items) > 0:
            for item in new_items:
                item['invoice'] = pk
            inv_detail_serializer = InvoiceDetailSerializer(data=new_items, many=True)
            if inv_detail_serializer.is_valid():
                inv_detail_serializer.save()
            else:
                return Response({'msg': 'Not valid'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'data': self.get_data(pk)}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            return Response({'msg': 'Not Found'}, status=status.HTTP_400_BAD_REQUEST)

        invoice.delete()
        return Response({'msg': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)





