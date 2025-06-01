from rest_framework import serializers
from .models import Client, Order, OrderLine
from employee.models import Employee

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name', 'ubication', 'position']

class OrderLineSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderLine
        fields = ['id', 'quantity', 'description', 'unit_price', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True, required=False)
    
    class Meta:
        model = Order
        fields = ['id', 'client', 'total', 'lines', 'anticipo', 'request_date', 'deadline', 'responsible']
    
    def create(self, validated_data):
        lines_data = validated_data.pop('lines', [])
        order = Order.objects.create(**validated_data)
        
        for line_data in lines_data:
            OrderLine.objects.create(order=order, **line_data)
        
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    lines = OrderLineSerializer(many=True)
    client_info = ClientSerializer(source='client', read_only=True)
    responsible_info = EmployeeSerializer(source='responsible', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'client_info', 'responsible_info', 'total', 'lines', 'anticipo', 'request_date', 'deadline']