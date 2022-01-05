from rest_framework import serializers


def not_equal(field1, field2, msg=None):
    def wrapper(data):
        value1 = data.get(field1)
        value2 = data.get(field2)
        if value1 == value2:
            raise serializers.ValidationError(
                msg or 'You cannot subscribe to yourself'
            )
    return wrapper
