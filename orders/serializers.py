from rest_framework import serializers
from .models import Client, Order, OrderLine

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone']

class OrderLineSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderLine
        fields = ['id', 'quantity', 'description', 'unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True, required=False)
    customer = serializers.CharField(source='client.name', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'client', 'customer', 'total', 'lines', 'anticipo', 'request_date', 'deadline']
    
    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        order = Order.objects.create(**validated_data)
        
        for line_data in lines_data:
            OrderLine.objects.create(order=order, **line_data)
        
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)
    customer = serializers.CharField(source='client.name', read_only=True)
    client_info = ClientSerializer(source='client', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'client', 'client_info', 'customer', 'total', 'lines', 'anticipo', 'request_date', 'deadline']