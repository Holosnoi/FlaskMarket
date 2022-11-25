from market import db, login_manager, app
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=False, default=1000)
    items = db.relationship("Item", backref="owned_user", lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __repr__(self):
        return f"Item - {self.name}"

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
    # item2 = Item(name="Laptop", price=1200, barcode="118224261413", description="desc1")
    # u1 = User(username="Maxim", email="maxim@gmail.com", password_hash="123456")

# with app.app_context():
        # # #     db.drop_all()
        # #     db.create_all()
        # #     db.session.add(u1)
        # #     db.session.add(item2)
        # #     db.session.commit()
        # #     print(Item.query.all())
        #     # for item in Item.query.filter_by(price=1200):
        #     #     print(item.name)
        #
        #     db.session.update()
        #     # db.session.add(item2)
        #     db.session.commit()
    # i = Item.query.filter_by(name="Laptop").first()
    # i.owner = User.query.filter_by(username="Maxim").first().id
    # i.price = 1000
    # db.session.add(i)
    # db.session.commit()
    # print(i.owned_user)
