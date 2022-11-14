from rest_framework import serializers


class CategoryRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        model = self.queryset.model
        return model.objects.get(name=data)

    def to_representation(self, value):
        return value.name


class IngredientRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        model = self.queryset.model
        return model.objects.filter(name__in=data).all()

    def to_representation(self, value):
        return [ingr.name for ingr in value.all()]