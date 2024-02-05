import graphene
from graphene_django import DjangoObjectType

from cookbook.models import Category, Ingredient

from django.core.exceptions import ObjectDoesNotExist 


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")




class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")



class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(CategoryType, name=graphene.String(required=True))
    all_categories = graphene.List(CategoryType)
    ingredient_by_name = graphene.Field(IngredientType, name=graphene.String(required=True))



    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related("category").all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        
        except Exception as e:
                # Handle other exceptions or log them
            return (e.message)
    def resolve_all_categories(root, info):
        # We can easily optimize query count in the resolve method
        return Category.objects.all()

    def resolve_ingredient_by_name(root,info, name):
        return Ingredient.objects.get(name=name)


schema = graphene.Schema(query=Query)