from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Simple API',
          description='A simple API with GET and POST endpoints')

ns = api.namespace('items', description='Item operations')

item_model = api.model('Item', {
    'id': fields.Integer(readonly=True, description='The item unique identifier'),
    'name': fields.String(required=True, description='The item name'),
})

items = []

@ns.route('/')
class ItemList(Resource):
    @ns.doc('list_items')
    @ns.marshal_list_with(item_model)
    def get(self):
        """List all items"""
        return items

    @ns.doc('create_item')
    @ns.expect(item_model)
    @ns.marshal_with(item_model, code=201)
    def post(self):
        """Create a new item"""
        new_item = api.payload
        new_item['id'] = len(items) + 1
        items.append(new_item)
        return new_item, 201

@ns.route('/<int:id>')
@ns.response(404, 'Item not found')
@ns.param('id', 'The item identifier')
class Item(Resource):
    @ns.doc('get_item')
    @ns.marshal_with(item_model)
    def get(self, id):
        """Fetch an item given its identifier"""
        for item in items:
            if item['id'] == id:
                return item
        api.abort(404, f"Item {id} doesn't exist")

if __name__ == '__main__':
    app.run(debug=True)
