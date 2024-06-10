from datetime import datetime

from rest_framework import serializers

from src.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['uuid', 'title', 'description', 'customer', 'employee', 'created_at', 'updated_at', 'closed_at',
                  'report', 'status']


class CreateTaskByEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'customer']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['employee'] = user
        return super().create(validated_data)


class CreateTaskByCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['customer'] = user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Task
        fields = ['uuid', 'title', 'description',]


class CompleteTaskSerializer(serializers.ModelSerializer):
    report = serializers.CharField(required=True)

    class Meta:
        model = Task
        fields = ('report',)

    def update(self, instance, validated_data):
        if instance.employee != self.context['request'].user:
            raise serializers.ValidationError({'error': 'You are not the assigned employee for this task'})

        instance.closed_at = datetime.now()
        instance.status = 'done'
        instance.report = validated_data['report']
        instance.save()
        return instance
