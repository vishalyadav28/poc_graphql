# Django GraphQL API Project

This is a simple Django project showcasing the implementation of a GraphQL API using the `graphene-django` library. The project includes models for ingredients and categories, and two GraphQL queries: `all_ingredients` and `category_by_name`.

# Query Example

all_ingredients

```query {
  allIngredients {
    id
    name
    category {
      id
      name
    }
    # Add other fields you want to retrieve
  }
}
```

category_by_name
```
query {
  categoryByName(name: "YourCategoryName") {
    id
    name
    # Add other fields you want to retrieve
  }
}
```
