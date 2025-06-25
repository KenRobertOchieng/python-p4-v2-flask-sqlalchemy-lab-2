from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)

    # reviews relationship
    reviews = db.relationship(
        'Review',
        back_populates='customer',
        cascade='all, delete-orphan'
    )

    # association proxy to get items directly
    items = association_proxy('reviews', 'item')

    # serialization rules to avoid recursion
    serialize_rules = (
        '-reviews.customer',
    )


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=True)

    # reviews relationship
    reviews = db.relationship(
        'Review',
        back_populates='item',
        cascade='all, delete-orphan'
    )

    # serialization rules to avoid recursion
    serialize_rules = (
        '-reviews.item',
    )


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    # relationships
    customer = db.relationship(
        'Customer',
        back_populates='reviews'
    )
    item = db.relationship(
        'Item',
        back_populates='reviews'
    )

    # serialization rules to avoid recursion
    serialize_rules = (
        '-customer.reviews',
        '-item.reviews',
    )

# End of models.py