from rest_framework import serializers
from .models import Invoice, InvoiceDetail


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

    def create(self, validated_data):
        validated_data['price'] = validated_data['unit_price']*validated_data['quantity']
        return InvoiceDetail.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.price = validated_data.get('unit_price', instance.unit_price)*validated_data.\
            get('quantity', instance.quantity)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.unit_price = validated_data.get('unit_price', instance.unit_price)
        instance.save()
        return instance


class InvoicedetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        exclude = ('id', 'invoice')
