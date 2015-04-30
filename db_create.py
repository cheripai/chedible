from project import db
from project.schema import Dish

db.create_all()

# Adding a test dish
dish = Dish('test', price=12.34, image='test', beef=None, dairy=None, egg=None, fish=True, gluten=True, meat=False, nut=True, pork=False, poultry=False, shellfish=True, soy=False, wheat=True, notes='awesome sauce', restaurant_id=1)

db.session.add(dish)
db.session.commit()
