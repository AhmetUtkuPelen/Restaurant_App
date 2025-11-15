from Models.PRODUCT.BaseProduct.BaseProductModel import Product
from sqlalchemy import CheckConstraint, Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Utils.Enums.Enums import DessertType
from sqlalchemy import Enum as SAEnum

class Dessert(Product):
    __tablename__ = "desserts"

    __table_args__ = (
        CheckConstraint('is_vegan IN (0, 1)', name='check_is_vegan'),
        CheckConstraint('is_alergic IN (0, 1)', name='check_is_alergic'),
        CheckConstraint('calories IS NOT NULL', name='check_calories'),
        {'extend_existing': True}
    )
    
    __mapper_args__ = {
        'polymorphic_identity': 'dessert',
    }
    
    id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    is_vegan = Column(Boolean, nullable=False)
    is_alergic = Column(Boolean, nullable=False)
    dessert_type = Column(SAEnum(DessertType, native_enum=False), nullable=False)
    calories = Column(Integer, nullable=False)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "is_vegan": self.is_vegan,
            "is_alergic": self.is_alergic,
            "dessert_type": self.dessert_type.value if hasattr(self.dessert_type, "value") else self.dessert_type,
            "calories": self.calories,
        })
        return base_dict

    def __repr__(self):
        return f"<Dessert(name={self.name}, is_vegan={self.is_vegan}, is_alergic={self.is_alergic}) | {self.dessert_type.value} | {self.calories} cal>"

    def __str__(self):
        return self.name

    def summary(self):
        return f"{self.name} | {self.is_vegan} | {self.is_alergic} | {self.supplier.name} | {self.dessert_type.value} | {self.calories} cal"

    @property
    def alergen_warning(self):
        if self.is_alergic == True:
            raise ValueError(f"{self.name} might contain alergic ingredients , please be careful !")
        else:
            return f"{self.name} is safe to eat"

    @property
    def vegan_warning(self):
        if self.is_vegan == True:
            return f"{self.name} is vegan"
        else:
            raise ValueError(f"{self.name} is not vegan , please be careful !")