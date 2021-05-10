from flask import Flask, request, render_template, redirect, flash, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = 'passkey'
debug = DebugToolbarExtension(app)

def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dictionary"""

    return {
        'id': cupcake.id,
        'flavor': cupcake.flavor,
        'size': cupcake.size,
        'rating': cupcake.rating,
        'image': cupcake.image
    }

###########
#API routes
###########

@app.route('/api/cupcakes', methods=['GET'])
@cross_origin()
def get_cupcakes():
    
    """Get all cupcakes"""

    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.route('/api/cupcakes/<int:cupcake_id>')
@cross_origin()
def get_cupcake_data(cupcake_id):
    """Get more info on a cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake=serialized)

@app.route('/api/cupcakes', methods=['POST'])
@cross_origin()
def create_cupcake():
    """New cupcake POST request"""
    
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return( jsonify(cupcake=serialized), 201 )

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
@cross_origin()
def update_cupcake(cupcake_id):
    """Update cupcake PATCH request"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return(jsonify(serialized))

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
@cross_origin()
def delete_cupcake(cupcake_id):
    """Delete cupcake DELETE request"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return(jsonify({'message': 'Deleted'}))



#######
#routes
#######

@app.route('/')
def homepage():

    return render_template('home.html')