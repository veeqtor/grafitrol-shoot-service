from flask_restplus import Resource

from main import endpoint
from src.models import User
from src.schemas.user import UserSchema


@endpoint('/user')
class UserView(Resource):
    def get(self):
        user = User.query.all()
        schema = UserSchema(many=True)
        data = schema.response_data(user, 'Fetched Users')

        return data, 200
