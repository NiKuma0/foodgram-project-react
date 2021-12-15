import json

from rest_framework import serializers


class SerializerRaelatedField(serializers.RelatedField):
    def __init__(self, serializer_class,
                 create=True, model=None, **kwargs):
        self.serializer_class = serializer_class
        self.model = model or serializer_class.Meta.model
        self.create = create
        super().__init__(**kwargs)

    def to_representation(self, value):
        serializer = self.serializer_class(
            instance=value
        )
        return serializer.data

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = json.loads(data.replace("'", "\""))
        serializer: serializers.Serializer = self.serializer_class(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        if not self.create:
            data = serializer .validated_data
            print(data)
            return self.model.objects.get(**data)
        # print(serializer)
        serializer.save()
        return serializer.instance

    def get_queryset(self):
        return self.model.objects.all()


class Tag(serializers.ListField):
    def __init__(self, model, *args, **kwargs):
        self.Model = model
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        return self.Model.objects.filter(pk__in=data)

    def to_representation(self, data):
        return [
            self.child.to_representation(item) if item is not None else None
            for item in data.all()
        ]
