from .base_model import BaseModel, db


class Recipe(BaseModel):
    """Recipe model"""

    __tablename__ = 'recipe'

    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    user_id = db.Column(
        db.String(22),
        db.ForeignKey('user.id'),
        nullable=False
    )

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def format(self):
        """Convert the recipe object to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ingredients": self.ingredients,
            "instructions": self.instructions,
            "user_id": self.user_id
        }
    
    @classmethod
    def find_recipe_by(cls, **kwargs):
        """Find the first recipe based on the provided filters"""
        return cls.query.filter_by(**kwargs).first()