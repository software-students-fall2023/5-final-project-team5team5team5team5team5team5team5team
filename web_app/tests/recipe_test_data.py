"""test data for recipe tests"""

TEST_REC = {
    "creditsText": "foodista.com",
    "sourceName": "foodista.com",
    "pricePerServing": 275.03,
    "extendedIngredients": [
        {
            "id": 1006615,
            "name": "flavor concentrated seafood broth",
            "nameClean": "stock",
            "original": "2 packets Swanson® Flavor Concentrated Seafood Broth",
            "originalName": "Swanson® Flavor Concentrated Seafood Broth",
            "amount": 2.0,
            "unit": "packets",
        },
    ],
    "id": 639413,
    "title": "Cilantro Lime Fish Tacos",
    "readyInMinutes": 45,
    "servings": 4,
    "sourceUrl": "http://www.foodista.com/recipe/Z7RHNQ7Z/cilantro-lime-fish-tacos",
    "image": "https://spoonacular.com/recipeImages/639413-556x370.jpg",
    "imageType": "jpg",
    "nutrition": {
        "nutrients": [
            {
                "name": "Calories",
                "amount": 455.84,
                "unit": "kcal",
                "percentOfDailyNeeds": 22.79,
            },
            {"name": "Fat", "amount": 23.58, "unit": "g", "percentOfDailyNeeds": 36.27},
            {
                "name": "Saturated Fat",
                "amount": 5.81,
                "unit": "g",
                "percentOfDailyNeeds": 36.3,
            },
            {
                "name": "Carbohydrates",
                "amount": 33.04,
                "unit": "g",
                "percentOfDailyNeeds": 11.01,
            },
            {
                "name": "Net Carbohydrates",
                "amount": 30.32,
                "unit": "g",
                "percentOfDailyNeeds": 11.02,
            },
            {"name": "Sugar", "amount": 4.03, "unit": "g", "percentOfDailyNeeds": 4.48},
            {
                "name": "Cholesterol",
                "amount": 65.18,
                "unit": "mg",
                "percentOfDailyNeeds": 21.73,
            },
            {
                "name": "Sodium",
                "amount": 616.1,
                "unit": "mg",
                "percentOfDailyNeeds": 26.79,
            },
            {
                "name": "Protein",
                "amount": 28.53,
                "unit": "g",
                "percentOfDailyNeeds": 57.05,
            },
            {
                "name": "Fiber",
                "amount": 2.73,
                "unit": "g",
                "percentOfDailyNeeds": 10.91,
            },
        ],
        "caloricBreakdown": {
            "percentProtein": 24.89,
            "percentFat": 46.28,
            "percentCarbs": 28.83,
        },
    },
    "summary": "tacos",
    "cuisines": ["Mexican"],
    "dishTypes": ["lunch", "main course", "main dish", "dinner"],
    "diets": ["pescatarian"],
    "instructions": "cook",
    "analyzedInstructions": [
        {
            "name": "",
            "steps": [
                {
                    "number": 1,
                    "step": "Heat the oil in a 12-inch skillet over medium-high heat.",
                    "ingredients": [
                        {
                            "id": 4582,
                            "name": "cooking oil",
                            "localizedName": "cooking oil",
                            "image": "vegetable-oil.jpg",
                        }
                    ],
                    "equipment": [
                        {
                            "id": 404645,
                            "name": "frying pan",
                            "localizedName": "frying pan",
                            "image": "pan.png",
                        }
                    ],
                },
            ],
        }
    ],
    "spoonacularSourceUrl": "https://spoonacular.com/cilantro-lime-fish-tacos-639413",
}
