from pprint import pprint

from rest_framework import serializers


class TagField(serializers.PrimaryKeyRelatedField):
    def __init__(self, child, *args, **kwargs):
        self.child = child
        super().__init__(*args, **kwargs)

    def to_representation(self, data):
        return self.child.to_representation(data)


class SerializerField(serializers.Field):
    def __init__(self, serializer_class, many=False, *args, **kwargs):
        self.serializers_class = serializer_class
        self.many = many
        super().__init__(*args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        return self.serializers_class(*args, **kwargs, many=self.many)

    def to_representation(self, value):
        return self.get_serializer(instance=value).data

    def to_internal_value(self, data):
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return instance
