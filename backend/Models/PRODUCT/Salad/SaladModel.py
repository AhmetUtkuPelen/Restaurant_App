from backend.Models.PRODUCT.BaseProduct.BaseProductModel import Product
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from Database.Database import Base


class Salad(Product):
    __tablename__ = 'salads'

    __table_args__ = (
        CheckConstraint('is_vegan IS NOT NULL', name='check_salad_is_vegan'),
        CheckConstraint('is_alergic IS NOT NULL', name='check_salad_is_alergic'),
        CheckConstraint('preperation_time IS NOT NULL', name='check_salad_preperation_time'),
        {'extend_existing': True}
    )

    __mapper_args__ = {
        'polymorphic_identity': 'salad',
    }

    id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    is_vegan = Column(Boolean, default=False, nullable=False)
    is_alergic = Column(Boolean, default=False, nullable=False)
    calories = Column(Integer, nullable=True, default=0)

    # -----------------------
    # Utility methods for ingredients
    # -----------------------

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "is_vegan": self.is_vegan,
            "is_alergic": self.is_alergic,
            "calories": self.calories,
        })
        return base_dict

    def summary(self) -> str:
        return f"{self.name} | {self.description} | {self.calories} cal"

    def __repr__(self):
        return f"<Salad(name={self.name}, is_vegan={self.is_vegan})>"

    def __str__(self):
        return self.name