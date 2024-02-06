import graphene
from graphene_django import DjangoObjectType
from cookbook.models import Category, Ingredient
from django.core.exceptions import ObjectDoesNotExist 
from graphql import GraphQLError
from django.shortcuts import get_object_or_404



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
    ingredient_by_id = graphene.Field(IngredientType, id=graphene.Int(required=True))
    categories_by_id = graphene.Field(CategoryType, id=graphene.Int(required=True))


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


    def resolve_categories_by_id(root,info,id):
        return Category.objects.get(pk=id)
    def resolve_ingredient_by_id(root,info,id):
        return Ingredient.objects.get(pk=id)    
        
class CategoryMutation(graphene.Mutation):
    # Define the arguments for the mutation
    class Arguments:
        old_name = graphene.String(required=True)
        new_name = graphene.String(required=True)

    # Define the fields returned by the mutation
    category = graphene.Field(CategoryType)
    created = graphene.Boolean()

    # Mutate method to create or update the category
    @classmethod
    def mutate(cls, root, info, old_name, new_name):
        # Check if a category with the old name already exists
        category, created = Category.objects.get_or_create(name=old_name)
        
        # Check if the new name already exists in the database
        if Category.objects.filter(name=new_name).exists():
            return GraphQLError("Category with new name already exists")

        # Update the category with the new name
        if not created:
            # Check if the new name is different from the old name
            if category.name != new_name:
                category.name = new_name
                category.save()
                return CategoryMutation(category=category, created=False)
            else:
                # If the new name is the same as the old name, return the category without updating
                return CategoryMutation(category=category, created=False)
        else:
            # If the category was created, return it with the 'created' flag set to true
            return CategoryMutation(category=category, created=True)


class CategoryIDMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)
        
    category = graphene.Field(CategoryType)
    

    @classmethod
    def mutate(cls, root, info, name, id):
        category = get_object_or_404(Category,id=id)
        category.name = name
        category.save()
        return CategoryIDMutation(category=category)


class DeleteCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls,root,info,id):
        category = get_object_or_404(Category,id=id)
        category.delete()
        return CategoryIDMutation(category=category)



class Mutation(graphene.ObjectType):
    #define mutation and creating class that handles creation or updation of category (here : CategoryMutation)
    update_category = CategoryMutation.Field()
    update_category_by_id = CategoryIDMutation.Field()
    delete_category_by_id = DeleteCategoryMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)