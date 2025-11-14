# Models/Product/Doner/Doner.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, CheckConstraint, JSON
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from backend.Models.PRODUCT.BaseProduct.BaseProductModel import Product
from Utils.Enums.Enums import SpiceLevel, MeatType, KebabSize
from sqlalchemy import Enum as SAEnum

class Kebab(Product):
    __tablename__ = "kebabs"

    __table_args__ = (
        CheckConstraint('meat_type IS NOT NULL'),
        CheckConstraint('spice_level IS NOT NULL'),
        CheckConstraint('is_vegan IS NOT NULL'),
        CheckConstraint('is_alergic IS NOT NULL'),
        CheckConstraint('preperation_time IS NOT NULL'),
        {'extend_existing': True}
    )

    __mapper_args__ = {
        'polymorphic_identity': 'kebab',
    }

    id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    size = Column(SAEnum(KebabSize, native_enum=False), nullable=False, default=KebabSize.MEDIUM)
    meat_type = Column(SAEnum(MeatType, native_enum=False), nullable=False)
    spice_level = Column(SAEnum(SpiceLevel, native_enum=False), nullable=False, default=SpiceLevel.MEDIUM)
    is_vegan = Column(Boolean, default=False, nullable=False)
    is_alergic = Column(Boolean, default=False, nullable=False)

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "size": self.size.value if hasattr(self.size, "value") else self.size,
            "meat_type": self.meat_type.value if hasattr(self.meat_type, "value") else self.meat_type,
            "spice_level": self.spice_level.value if hasattr(self.spice_level, "value") else self.spice_level,
            "is_vegan": self.is_vegan,
            "is_alergic": self.is_alergic,
        })
        return base_dict

    # -----------------------
    # Utility methods
    # -----------------------

    async def summary(self) -> str:
        return f"{self.name} {self.meat_type.value.title()}, {self.spice_level.value.lower()} spice"

    @property
    def description_summary(self):
        return f"{self.meat_type.value.title()} kebab with {self.spice_level.value.lower()} spices."

    def __repr__(self):
        return f"<Kebab(name={self.name}, meat_type={self.meat_type}, spice={self.spice_level})>"

    def __str__(self):
        return f"{self.name} {self.meat_type.value.title()}, {self.spice_level.value.lower()} spice, {self.size.value.title()})"