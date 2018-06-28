from flask import Flask 
from flask_restful import Resource, Api, request
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
api = Api(app)
app.secret_key = "hunter"

jwt = JWT(app, authenticate, identity) #/auth

items = []


class Item(Resource):
	@jwt_required()
	def get(self, name):

		item = next(filter(lambda x: x['name'] == name, items), None)

		return {"item": item}, 200 if item else 404

	
	def post(self, name):
		if next(filter(lambda x: x['name'] == name, items), None):

			return {"message": "An item with name '{}' already exists.".format(name)}, 400

		data = request.get_json(silent=True)

		item = {"name": name, "price": data["price"]}
		items.append(item)

		return item, 201

	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] !=name, items))
		return {"message": "Item Deleted"}

	def put(self, name):
		data = request.get_json()
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None: 
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)

		return item

class ItemList(Resource):
	
	def get(self):

		return {"items": items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items")

app.run(port=3000, debug = True)