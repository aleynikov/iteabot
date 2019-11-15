from mongoengine import connect
import models


connect('telegram')

# for i in range(5):
#     obj = models.Category(**{'title': f'root {i}', 'descr': f'descr {i}'}).save()

#     obj.add_subcategory(
#         models.Category(**{'title': f'sub {i}', 'descr': f'descr {i}'})
#     )

objects = models.Category.objects(parent__ne=None)
for o in objects:
    o.add_subcategory(
        models.Category(**{'title': f'sub-sub {o}', 'descr': f'descr {o}'})
    )
