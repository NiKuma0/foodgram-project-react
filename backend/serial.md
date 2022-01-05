# User serializers:

## User serializer:
* fields: ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

for **get users view**, **registration** and for **field author of recipe**

## Verbose User serializer:
* fields: 
('email', 'id', 'username', 'first_name', 
'last_name', 'is_subscribed', 'recipe_count', 
['recipes'](##-include-recipe-serializer:))
* detail: recipes field it is serializer (`many=True`) of Recipe model

for **subscription view**

# Tag Serializers:

## Tag serializer:
* fields: ('id', 'name', 'color', 'slug')

for **Tag view**

# Recipe Serializers:

## Recipe Serializer:
* fields: 
('id', ['tags'](##-tag-serializer:), ['author'](##-user-serializer:), 
['ingredients'](##-ingredients-serializer:), 'is_favorited', 
'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

for **Recipe view**

## Include Recipe Serializer:
* fields: ('id', 'name', 'image', 'cooking_time')

For other serializers. Uses as related field

# Ingredients Serializers:

## Ingredient Serializer:

* fields: ('id', 'name', 'measurement_unit')

for **Ingredient View**

## Creation Ingredient Serializer:
* fields: ('id', 'amount') 
* detail: 'id' is the ingredient choice field
