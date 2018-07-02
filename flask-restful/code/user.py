import sqlite3
from flask_restful import Resource, reqparse

class User:
	def __init__(cls, _id, username, password):
		cls.id = _id
		cls.username = username
		cls.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username=?"
		result = cursor.execute(query, (username,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else: 
			user = None

		connection.close()
		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id=?"
		result = cursor.execute(query, (_id,))
		row = result.fetchone()
		if row:
			user = cls(*row)
		else: 
			user = None

		connection.close()
		return user

class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('username',
		type=str,
		required=True,
		help="This field cannot be left blank."
	)
	parser.add_argument('password',
		type=str,
		required=True,
		help="this field cannot be left blank."
	)

	def post(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		data = UserRegister.parser.parse_args()

		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data["username"], data["password"]))

		connection.commit()
		connection.close()

		return {"message": "User created successfully."}, 201