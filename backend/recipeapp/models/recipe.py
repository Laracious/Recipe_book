from .base_model import BaseModel, db
from json import JSONEncoder


class Recipe(BaseModel):
    """Recipe model"""

    __tablename__ = 'recipe'

    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    user_id = db.Column(
        db.String(22), 
        db.ForeignKey('user.id'), 
        nullable=False
        )

    # Additional fields
    video = db.Column(db.String(255), nullable=True)
    user_rating = db.Column(
        db.JSON, nullable=True,
        default={"positive": 0, "negative": 0, "score": 0}
        )
    ingredients = db.Column(db.JSON, nullable=True)
    image = db.Column(db.String(255), nullable=True)

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = kwargs.get('description')
        self.instructions = kwargs.get('instructions')
        self.user_id = kwargs.get('user_id')
        self.video = kwargs.get('video')
        self.user_rating = kwargs.get(
            'user_rating',
            {"positive": 0, "score": 0, "negative": 0}
            )
        self.ingredients = kwargs.get('ingredients')
        self.image = kwargs.get('image')

    def format(self):
        """Convert the recipe object to a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instructions": self.instructions,
            "user_id": self.user_id,
            "video": self.video,
            "user_rating": self.user_rating,
            "ingredients": self.ingredients,
            "image": self.image
            }

    def add_positive_rating(self):
        """Increment positive user rating count and update the score"""
        self.user_rating["count_positive"] += 1
        self.update_score()

    def add_negative_rating(self):
        """Increment negative user rating count and update the score"""
        self.user_rating["count_negative"] += 1
        self.update_score()
    
    def update_score(self):
        """Calculate the score based on positive and negative ratings"""
        total_ratings = (
            self.user_rating["count_positive"] + self.user_rating["count_negative"]
            )
        if total_ratings > 0:
            self.user_rating["score"] = round(
                (self.user_rating["count_positive"] / total_ratings) * 100, 6
                )
        else:
            self.user_rating["score"] = 0
    
    # def update_score(self):
    #     """Calculate the score based on positive and negative ratings"""
    #     total_ratings = (
    #         self.user_rating["count_positive"] + self.user_rating["count_negative"]
    #     )
    #     self.user_rating["score"] = (
    #         self.user_rating["count_positive"] / max(1, total_ratings) * 100 
    #     )
    
    # @classmethod
    # def find_recipe_by(cls, **kwargs):
    #     """Find the first recipe based on the provided filters"""
    #     return cls.query.filter_by(**kwargs).first()
    