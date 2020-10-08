from server import db, ma
from datetime import datetime

#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(50))
    phonenumber = db.Column(db.String(20))
    address = db.Column(db.String(200))
    password = db.Column(db.String(20))
    code = db.Column(db.String(20))
    lx = db.Column(db.Float)
    ly = db.Column(db.Float)
    permission = db.Column(db.Integer, default=0)
    date_register = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, username, email, phonenumber, address, password, code, lx, ly, permission):
        self.username = username
        self.email = email
        self.phonenumber = phonenumber
        self.address = address
        self.password = password
        self.code = code
        self.lx = lx
        self.ly = ly
        self.permission = permission

#schema user
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'phonenumber', 'address', 'password', 'code','lx', 'ly', 'permission', 'date_register')

userSchema = UserSchema()
usersSchema = UserSchema(many = True)

#Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sicknessId = db.Column(db.Integer)
    image_file = db.Column(db.String(20))
    lx = db.Column(db.Float)
    ly = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, sicknessId, image_file, lx, ly, user_id):
        self.sicknessId = sicknessId
        self.image_file = image_file
        self.lx = lx
        self.ly = ly
        self.user_id = user_id

#Post schema
class PostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sicknessId', 'image_file', 'lx', 'ly', 'user_id', 'date_posted')

postSchema = PostSchema()
postsSchema = PostSchema(many = True)

#sickness model
class Sickness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(200))
    solution = db.Column(db.String(1000))

    def __init__(self, name, description, solution):
        self.name = name
        self.description = description
        self.solution = solution

#schema sickness
class SicknessSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'desciption', 'solution')

sicknessSchema = SicknessSchema()
sicknessesSchema = SicknessSchema(many = True)

#Department model
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    address = db.Column(db.String(200))
    phonenumber = db.Column(db.String(20))
    email = db.Column(db.String(50))
    jurisdiction = db.Column(db.Integer)

    def __init__(self, name, address, phonenumber, email, jurisdiction):
        self.name = name
        self.address = address
        self.phonenumber = phonenumber
        self.email = email
        self.jurisdiction = jurisdiction

#schema departments
class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'phonenumber', 'jurisdiction')

departmentSchema = DepartmentSchema()
departmentsSchema = DepartmentSchema(many = True)

#Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500))
    price = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    store = db.Column(db.Integer, db.ForeignKey("user.id"))
    images = db.Column(db.String(10))
    types = db.Column(db.String(20))
    brand = db.Column(db.String(50))
    source = db.Column(db.String(50))
    date_update = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __init__(self, name, desciption, price, quantity, store, images, types, brand, source):
        self.name = name
        self.description = desciption
        self.price = price
        self.quantity = quantity
        self.store = store
        self.images = images
        self.types = types
        self.brand = brand
        self.source = source

#schema product
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'quantity', 'store', 'images', 'types', 'brand', 'source')

productSchema = ProductSchema()
productsSchema = ProductSchema(many = True)

#Bill model
class Bill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"))
    storeId = db.Column(db.Integer, db.ForeignKey("user.id"))
    totalPrice = db.Column(db.String(10))
    lx = db.Column(db.Float)
    ly = db.Column(db.Float)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(15))
    status = db.Column(db.Integer, default = 0)
    date_register = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, userId, storeId, totalPrice, lx, ly, address, phone):
        self.userId = userId
        self.storeId = storeId
        self.totalPrice = totalPrice
        self.lx = lx
        self.ly = ly
        self.address = address
        self.phone = phone

#schema bill
class BillSchema(ma.Schema):
    class Meta:
        fields = ('id', 'userId', 'storeId','totalPrice', 'lx', 'ly', 'address', 'phone', 'status', 'date_register')

billSchema = BillSchema()
billsSchema = BillSchema(many = True)

#bill_detail model
class Bill_detail(db.Model):
    bdId = db.Column(db.Integer, primary_key=True)
    bId = db.Column(db.Integer, db.ForeignKey("bill.id"))
    pId = db.Column(db.Integer, db.ForeignKey("product.id"))
    quantity = db.Column(db.Integer)

    def __init__(self, bId, pId, quantity):
        self.bId = bId
        self.pId = pId
        self.quantity = quantity

#schema bill_detail
class BillDetailSchema(ma.Schema):
    class Meta:
        fields = ('bId', 'pId', 'quantity')

billDetailSchema = BillDetailSchema()
billDetailsSchema = BillDetailSchema(many = True)

