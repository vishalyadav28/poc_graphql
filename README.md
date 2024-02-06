# Django GraphQL API Project

This is a simple Django project showcasing the implementation of a GraphQL API using the `graphene-django` library. The project includes models for ingredients and categories, and two GraphQL queries: `all_ingredients` and `category_by_name`.

# Query Example

# 1.
``` {
   allIngredients {
     id
     name
     notes
     category {
       name
     }
   }
 }
# output
 {
   "data": {
     "allIngredients": [
       {
         "id": "1",
         "name": "test1",
         "notes": "something",
         "category": {
           "name": "cat 1"
         }
       },
       {
         "id": "2",
         "name": "test2",
         "notes": "test",
         "category": {
           "name": "cat 2"
         }
       },
       {
         "id": "3",
         "name": "test3",
         "notes": "notes",
         "category": {
           "name": "cat 3"
         }
       },
       {
         "id": "4",
         "name": "test4",
         "notes": "notes",
         "category": {
           "name": "cat 1"
         }
       },
       {
         "id": "5",
         "name": "test5",
         "notes": "notes",
         "category": {
           "name": "cat 1"
         }
       }
     ]
   }
 }

```

# 2.
``` {
   categoryByName(name: "cat 1"){
     name
     ingredients {
       name
     }
   }
 }

 output
 {
   "data": {
     "categoryByName": {
       "name": "cat 1",
       "ingredients": [
         {
           "name": "test1"
         },
         {
           "name": "test4"
         },
         {
           "name": "test5"
         }
       ]
     }
   }
 }
```


# 3.
``` {
   allCategories {
     name
     ingredients {
       name
     }
   }
 }

# ouptut
 {
   "data": {
     "allCategories": [
       {
         "name": "cat 1",
         "ingredients": [
           {
             "name": "test1"
           }
         ]
       },
       {
         "name": "cat 2",
         "ingredients": [
           {
             "name": "test2"
           }
         ]
       },
       {
         "name": "cat 3",
         "ingredients": [
           {
             "name": "test3"
           }
         ]
       }
     ]
   }
 }
```

# 4.

```
 {
   ingredientByName(name: "test1") {
     id
     name
     notes
     category {
       id
       name
     }
   }
 }

#output

 {
   "data": {
     "ingredientByName": {
       "id": "1",
       "name": "test1",
       "notes": "something",
       "category": {
         "id": "1",
         "name": "cat 1"
       }
     }
   }
 }
 ```


# Mutation example

```
create if not available else update

mutation{
  updateCategory(oldName: "new cat", newName:"updated cat"){
    category{
      id
      name
    }
  }

}

# output

{
  "data": {
    "updateCategory": {
      "category": {
        "id": "6",
        "name": "updated cat 1"
      }
    }
  }
}



```




# 2 (update)

mutation {
  updateCategoryById(id: 5, name: "bla bla") {
    category {
      name
    }
  }
}

#output
{
  "data": {
    "updateCategoryById": {
      "category": {
        "name": "bla bla"
      }
    }
  }
}



# 3 delete

mutation {
  deleteCategoryById(id:5) {
    category {
      name
    }
  }
}

#output

{
  "data": {
    "deleteCategoryById": {
      "category": {
        "name": "bla bla"
      }
    }
  }
}


```

