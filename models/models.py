from mongoengine import *

connect('telegram')

class Texts(Document):
    title = StringField(unique=True)
    body = StringField(max_length=4096)

class Category(Document):
    title = StringField(max_length=255, required=True)
    descr = StringField(max_length=1024)
    subcategory = ListField(ReferenceField('self'))
    parent = ReferenceField('self')

    @classmethod
    def get_root_categories(cls):
        return cls.objects(parent=None)

    @property
    def is_root(self):
        return not bool(self.parent)

    @property
    def is_parent(self):
        return bool(self.subcategory)

    @property
    def get_products(self, **kwargs ):
        return Product.objects(category=self, **kwargs)

    def add_subcategory(self, obj):
        obj.parent = self
        obj.save()
        self.subcategory.append(obj)
        self.save()

class Properties(DynamicEmbeddedDocument):
    weight = FloatField(min_value=0)

class Product(Document):
    title = StringField(max_length=255)
    descr = StringField(max_length=1024)
    price = IntField(min_value=0)
    new_price = IntField(min_value=0)
    is_discount = BooleanField(default=False)
    props = EmbeddedDocumentField(Properties)
    category = ReferenceField(Category)

    @property
    def get_price(self):
        price = self.price
        if (self.is_discount):
            price = self.new_price
        return str(price / 100)
    
    @classmethod
    def get_discount_products(cls, **kwargs):
        return cls.objects(is_discount=True, **kwargs)


