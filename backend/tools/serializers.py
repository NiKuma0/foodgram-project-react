from rest_framework import serializers


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop('exclude', None)
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
