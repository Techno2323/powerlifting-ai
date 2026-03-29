"""
Dynamic diet builder - creates meals based on maintenance calories and goal
"""

def generate_diet_plan(bodyweight, height, age, goal, food_type, calories, protein, carbs, fats):
    """Generate personalized diet with proper macro distribution and alternatives"""
    
    # Determine meal frequency and calorie split
    meal_splits = {
        "8:00 AM Breakfast": 0.30,
        "11:00 AM Mid-Morning": 0.10,
        "1:30 PM Lunch": 0.30,
        "4:00 PM Pre-Workout": 0.10,
        "7:00 PM Post-Workout": 0.15,
        "9:30 PM Evening": 0.05
    }
    
    # Calculate calories per meal
    meal_cals = {time: int(calories * split) for time, split in meal_splits.items()}
    
    # Macro distribution per meal
    macro_splits = {
        "8:00 AM Breakfast": {"p_ratio": 0.25, "c_ratio": 0.50, "f_ratio": 0.25},
        "11:00 AM Mid-Morning": {"p_ratio": 0.30, "c_ratio": 0.50, "f_ratio": 0.20},
        "1:30 PM Lunch": {"p_ratio": 0.35, "c_ratio": 0.45, "f_ratio": 0.20},
        "4:00 PM Pre-Workout": {"p_ratio": 0.15, "c_ratio": 0.75, "f_ratio": 0.10},
        "7:00 PM Post-Workout": {"p_ratio": 0.40, "c_ratio": 0.45, "f_ratio": 0.15},
        "9:30 PM Evening": {"p_ratio": 0.35, "c_ratio": 0.40, "f_ratio": 0.25}
    }
    
    # Calculate macros per meal
    meal_macros = {}
    for time, cal in meal_cals.items():
        ratios = macro_splits[time]
        meal_macros[time] = {
            "cals": cal,
            "protein": int((cal * ratios["p_ratio"]) / 4),
            "carbs": int((cal * ratios["c_ratio"]) / 4),
            "fats": int((cal * ratios["f_ratio"]) / 9)
        }
    
    # Build meals based on food type
    if food_type == "Vegetarian":
        meals_db = build_vegetarian_meals(bodyweight, meal_macros)
    elif food_type == "Non-Vegetarian":
        meals_db = build_nonveg_meals(bodyweight, meal_macros)
    else:  # Eggetarian
        meals_db = build_eggetarian_meals(bodyweight, meal_macros)
    
    # Select best meal for each slot and get alternatives
    selected_meals = {}
    meal_alternatives = {}
    
    for time, target_macros in meal_macros.items():
        if time in meals_db:
            # Get best meal
            best_meal = find_best_meal(meals_db[time], target_macros)
            selected_meals[time] = best_meal
            
            # Store all alternatives
            meal_alternatives[time] = meals_db[time]
    
    return selected_meals, meal_macros, meal_alternatives


def find_best_meal(meal_options, target_macros):
    """Find meal closest to target macros"""
    
    def macro_distance(meal, target):
        p_diff = abs(meal["protein"] - target["protein"])
        c_diff = abs(meal["carbs"] - target["carbs"])
        f_diff = abs(meal["fats"] - target["fats"])
        return p_diff + c_diff + f_diff
    
    best = min(meal_options, key=lambda m: macro_distance(m, target_macros))
    return best


def build_vegetarian_meals(bw, meal_macros):
    """Generate vegetarian meal options"""
    
    return {
        "8:00 AM Breakfast": [
            {"food": "2 rotis + 200g paneer + 1 cup rice", "protein": 40, "carbs": 70, "fats": 20},
            {"food": "Oats (100g) + 2 eggs + banana + honey", "protein": 38, "carbs": 60, "fats": 18},
            {"food": "3 idlis + 200g curd + 1 tbsp peanut butter", "protein": 35, "carbs": 65, "fats": 16},
            {"food": "Upma (1.5 cups) + vegetables + curd", "protein": 32, "carbs": 68, "fats": 14},
            {"food": "Dosa (2) + sambar + curd", "protein": 30, "carbs": 72, "fats": 12}
        ],
        "11:00 AM Mid-Morning": [
            {"food": "1 cup yogurt + banana + 30g almonds", "protein": 15, "carbs": 30, "fats": 8},
            {"food": "Protein shake + apple + 20g mixed nuts", "protein": 18, "carbs": 28, "fats": 10},
            {"food": "200g cottage cheese + granola + honey", "protein": 20, "carbs": 32, "fats": 9},
            {"food": "Roasted chickpeas (150g) + banana", "protein": 16, "carbs": 26, "fats": 7},
            {"food": "Milk + protein powder + dates", "protein": 22, "carbs": 24, "fats": 5}
        ],
        "1:30 PM Lunch": [
            {"food": "2 rotis + 250g paneer curry + 1 cup rice", "protein": 55, "carbs": 70, "fats": 12},
            {"food": "3 cups dal + 3 rotis + rice + salad", "protein": 50, "carbs": 75, "fats": 10},
            {"food": "Chickpea curry + 2 rotis + 1 cup rice", "protein": 45, "carbs": 72, "fats": 11},
            {"food": "Rajma (3 cups) + 3 rotis + rice", "protein": 48, "carbs": 74, "fats": 9},
            {"food": "Mixed vegetable curry + 3 rotis + rice + curd", "protein": 40, "carbs": 76, "fats": 13}
        ],
        "4:00 PM Pre-Workout": [
            {"food": "2 slices bread + 2 tbsp peanut butter + banana", "protein": 10, "carbs": 50, "fats": 8},
            {"food": "Banana + energy bar + honey", "protein": 8, "carbs": 52, "fats": 5},
            {"food": "Rice cakes (3) + almond butter + dates", "protein": 9, "carbs": 48, "fats": 7},
            {"food": "Roti (2) + jaggery + banana", "protein": 6, "carbs": 54, "fats": 4},
            {"food": "Oats (50g) + banana + honey", "protein": 8, "carbs": 50, "fats": 3}
        ],
        "7:00 PM Post-Workout": [
            {"food": "1 scoop whey + rice (1 cup) + 200g paneer", "protein": 50, "carbs": 60, "fats": 8},
            {"food": "Protein smoothie + oats + banana + yogurt", "protein": 48, "carbs": 58, "fats": 7},
            {"food": "200g cottage cheese + rice + vegetables", "protein": 45, "carbs": 62, "fats": 6},
            {"food": "Khichdi (2 cups) + ghee + curd", "protein": 38, "carbs": 65, "fats": 10},
            {"food": "Upma (2 cups) + eggs (2) + curd", "protein": 44, "carbs": 60, "fats": 9}
        ],
        "9:30 PM Evening": [
            {"food": "2 rotis + 200g dal + salad", "protein": 25, "carbs": 50, "fats": 5},
            {"food": "Vegetable soup + 3 rotis + curd", "protein": 22, "carbs": 48, "fats": 4},
            {"food": "Quinoa (1 cup) + vegetables + yogurt", "protein": 28, "carbs": 52, "fats": 6},
            {"food": "2 rotis + moong dal sprouts + light curry", "protein": 24, "carbs": 48, "fats": 3},
            {"food": "Poha (1.5 cups) + vegetables + curd", "protein": 20, "carbs": 50, "fats": 4}
        ]
    }


def build_nonveg_meals(bw, meal_macros):
    """Generate non-veg meal options"""
    
    return {
        "8:00 AM Breakfast": [
            {"food": "3 eggs + 2 slices bread + 1 cup milk", "protein": 42, "carbs": 45, "fats": 18},
            {"food": "150g chicken breast + oats + banana", "protein": 45, "carbs": 50, "fats": 12},
            {"food": "Fish (150g) + 2 rotis + vegetables", "protein": 48, "carbs": 48, "fats": 14},
            {"food": "Scrambled eggs (4) + toast + butter + OJ", "protein": 40, "carbs": 52, "fats": 20},
            {"food": "Turkey sausage (200g) + pancakes + honey", "protein": 44, "carbs": 56, "fats": 16}
        ],
        "11:00 AM Mid-Morning": [
            {"food": "150g chicken breast + apple + almonds", "protein": 35, "carbs": 25, "fats": 10},
            {"food": "Protein shake + oats + honey", "protein": 32, "carbs": 28, "fats": 8},
            {"food": "Boiled eggs (3) + banana + peanut butter", "protein": 38, "carbs": 26, "fats": 12},
            {"food": "Tuna (120g) + rice cakes + honey", "protein": 28, "carbs": 30, "fats": 6},
            {"food": "Chicken (120g) + bread + cheese", "protein": 32, "carbs": 24, "fats": 11}
        ],
        "1:30 PM Lunch": [
            {"food": "250g chicken + 2 rotis + 1 cup rice", "protein": 60, "carbs": 75, "fats": 15},
            {"food": "300g fish + 2 rotis + rice + salad", "protein": 65, "carbs": 72, "fats": 18},
            {"food": "Lean beef (250g) + potatoes + vegetables", "protein": 58, "carbs": 70, "fats": 16},
            {"food": "Mutton curry (300g) + 3 rotis + rice", "protein": 55, "carbs": 78, "fats": 20},
            {"food": "Grilled chicken (300g) + rice + dal", "protein": 62, "carbs": 68, "fats": 12}
        ],
        "4:00 PM Pre-Workout": [
            {"food": "150g chicken + banana + bread", "protein": 32, "carbs": 48, "fats": 5},
            {"food": "Tuna (120g) + rice cakes + honey", "protein": 28, "carbs": 50, "fats": 6},
            {"food": "Boiled eggs (2) + sweet potato + dates", "protein": 26, "carbs": 45, "fats": 8},
            {"food": "Turkey breast (100g) + oats + banana", "protein": 30, "carbs": 48, "fats": 4},
            {"food": "Salmon (100g) + rice + honey", "protein": 28, "carbs": 46, "fats": 8}
        ],
        "7:00 PM Post-Workout": [
            {"food": "1 scoop whey + rice + 200g fish", "protein": 55, "carbs": 65, "fats": 10},
            {"food": "Protein shake + chicken (150g) + rice", "protein": 58, "carbs": 62, "fats": 9},
            {"food": "Lean beef (180g) + oats + banana", "protein": 52, "carbs": 58, "fats": 12},
            {"food": "Grilled chicken (200g) + sweet potato + curd", "protein": 50, "carbs": 60, "fats": 8},
            {"food": "Fish fillet (180g) + rice + vegetables", "protein": 48, "carbs": 64, "fats": 10}
        ],
        "9:30 PM Evening": [
            {"food": "150g chicken breast + 2 rotis + salad", "protein": 35, "carbs": 45, "fats": 5},
            {"food": "Fish (120g) + rice + vegetables", "protein": 30, "carbs": 48, "fats": 6},
            {"food": "Turkey (120g) + quinoa + vegetables", "protein": 32, "carbs": 50, "fats": 7},
            {"food": "Chicken (100g) + dal + 2 rotis", "protein": 28, "carbs": 46, "fats": 4},
            {"food": "Lean ground chicken (150g) + rice + salad", "protein": 33, "carbs": 48, "fats": 6}
        ]
    }


def build_eggetarian_meals(bw, meal_macros):
    """Generate eggetarian meal options"""
    
    return {
        "8:00 AM Breakfast": [
            {"food": "4 eggs + 2 rotis + 1 cup milk", "protein": 44, "carbs": 50, "fats": 20},
            {"food": "Omelette (3 eggs) + 2 slices bread + honey", "protein": 42, "carbs": 48, "fats": 18},
            {"food": "Scrambled eggs (4) + toast + butter + OJ", "protein": 40, "carbs": 52, "fats": 19},
            {"food": "Egg curry (4 eggs) + 2 rotis + rice", "protein": 42, "carbs": 58, "fats": 17},
            {"food": "Cheese omelette (3 eggs) + bread + vegetables", "protein": 38, "carbs": 50, "fats": 20}
        ],
        "11:00 AM Mid-Morning": [
            {"food": "200g curd + banana + granola", "protein": 18, "carbs": 32, "fats": 9},
            {"food": "3 boiled eggs + apple + almonds", "protein": 22, "carbs": 28, "fats": 11},
            {"food": "Protein shake + oats + berries", "protein": 20, "carbs": 30, "fats": 8},
            {"food": "Cheese + crackers + honey + banana", "protein": 16, "carbs": 34, "fats": 10},
            {"food": "Paneer (100g) + bread + jam", "protein": 20, "carbs": 32, "fats": 9}
        ],
        "1:30 PM Lunch": [
            {"food": "2 rotis + 200g paneer curry + 1 cup rice", "protein": 55, "carbs": 70, "fats": 12},
            {"food": "Egg curry (4 eggs) + 2 rotis + rice + salad", "protein": 52, "carbs": 72, "fats": 14},
            {"food": "Cheese omelette (3 eggs) + 2 rotis + rice + veg", "protein": 50, "carbs": 68, "fats": 16},
            {"food": "Paneer tikka masala + 3 rotis + rice", "protein": 48, "carbs": 70, "fats": 15},
            {"food": "Egg fried rice (3 cups) + vegetables + curd", "protein": 45, "carbs": 74, "fats": 13}
        ],
        "4:00 PM Pre-Workout": [
            {"food": "2 boiled eggs + banana + bread", "protein": 14, "carbs": 48, "fats": 7},
            {"food": "Cheese toast + honey + banana", "protein": 12, "carbs": 50, "fats": 9},
            {"food": "Protein shake + rice cakes + dates", "protein": 16, "carbs": 52, "fats": 6},
            {"food": "Omelette (2 eggs) + bread + jam + banana", "protein": 14, "carbs": 54, "fats": 8},
            {"food": "Paneer (80g) + bread + honey", "protein": 12, "carbs": 48, "fats": 8}
        ],
        "7:00 PM Post-Workout": [
            {"food": "Protein shake + rice + 200g paneer", "protein": 52, "carbs": 60, "fats": 10},
            {"food": "3 eggs + oats + banana + milk", "protein": 48, "carbs": 58, "fats": 12},
            {"food": "Cottage cheese (250g) + rice + berries", "protein": 50, "carbs": 62, "fats": 8},
            {"food": "Paneer tikka (250g) + rice + vegetables", "protein": 48, "carbs": 64, "fats": 11},
            {"food": "Egg biryani (2 cups) + curd", "protein": 46, "carbs": 66, "fats": 12}
        ],
        "9:30 PM Evening": [
            {"food": "2 rotis + 200g dal + egg + salad", "protein": 28, "carbs": 50, "fats": 6},
            {"food": "Veg soup + 2 rotis + boiled eggs (2)", "protein": 25, "carbs": 48, "fats": 5},
            {"food": "Quinoa (1 cup) + cheese + vegetables", "protein": 30, "carbs": 52, "fats": 7},
            {"food": "2 rotis + moong dal + boiled egg", "protein": 26, "carbs": 46, "fats": 4},
            {"food": "Paneer tikka (150g) + rice + salad", "protein": 28, "carbs": 50, "fats": 8}
        ]
    }