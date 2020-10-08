from server import app, db
import os
from server.models import User, Post, Product, Bill, Bill_detail, usersSchema, postsSchema, productsSchema, billsSchema, billDetailsSchema, Sickness, Department
import markdown
from flask import request, jsonify, render_template, send_file
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import cv2
import tensorflow as tf
import h5py
from server.unity import *

# load model
datamodel = h5py.File("E:\\dev\\chicken-app\\api\\chicken.h5", "r")
model = tf.keras.models.load_model(datamodel)
checkChicken = tf.keras.applications.resnet50.ResNet50(weights='imagenet')

# API
# @app.route("/", methods=["GET"])
# def home():
    # """Present some documentation"""

    # # Open the README file
    # with open(os.path.dirname(app.root_path) + '/Document.md', 'r') as markdown_file:

    #     # Read the content of the file
    #     content = markdown_file.read()

    #     # Convert to HTML
    #     return markdown.markdown(content)

# load images
@app.route("/images", methods=["GET"])
def send_images():
    image_name = get_queries(request)["image"]
    return send_file(f"./images/{image_name}", mimetype='image/gif')

# AUTH API
@app.route("/user/auth/register", methods=["POST"])
def register():
    data = request.json
    print(data)
    try:
        username = data.get("username")
        email = data.get("email")
        phonenumber = data.get("phonenumber")
        code = data.get("code")
        try:
            existUsername = User.query.filter_by(username=username).first()
            if existUsername:
                return jsonify(
                    success=False,
                    error="This username is alrealy exist"
                )

            existEmail = User.query.filter_by(email=email).first()
            if existEmail:
                return jsonify(
                    success=False,
                    error="This email is alrealy exist"
                )

            existPhonenumber = User.query.filter_by(
                phonenumber=phonenumber).first()
            if existPhonenumber:
                return jsonify(
                    success=False,
                    error="This phonenumber is alrealy exist"
                )

            existCode = User.query.filter_by(code=code).first()
            if existCode:
                return jsonify(
                    success=False,
                    error="This code is alrealy exist"
                )
        except:
            pass

        address = data.get("address")
        lx = data.get("lx")
        ly = data.get("ly")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            return jsonify(
                success=False,
                error="password not match"
            )
            
        newUser = User(username, email, phonenumber,
                       address, password, code, lx, ly, 0)
        try:
            db.session.add(newUser)
            db.session.commit()
            return jsonify(
                success=True,
            )
        except:
            return jsonify(
                success=False,
                error="cannot register"
            )

    except:
        return jsonify(
            success=False,
            error="cannot register"
        )

# user login
@app.route("/user/auth/login", methods=["POST"])
def login():
    print(request.values)
    email = request.json.get("email")
    print("Email: ", email)
    dataEmail = User.query.filter_by(email=email).first()
    if dataEmail:
        password = request.json.get("password")
        print("password: ", password)
        if password == dataEmail.password:
            return jsonify(
                success=True,
                username=dataEmail.username,
                id=dataEmail.id,
                permission=dataEmail.permission
            )
        else:
            return jsonify(
                success=False,
                error="password is not correct"
            )
    else:
        return jsonify(
            success=False,
            error="This email does not exist"
        )

# PRODUCT API
# Get products
@app.route("/user/product/getProducts", methods=["GET"])
def get_products():
    queries = get_queries(request)
    products = Product.query.all()
    all_products = format_products_list(
        filter_arr_by_queries(productsSchema.dump(products), queries))
    if len(all_products) == 0:
        return jsonify(
            message="don't have any products!"
        )
    else:
        return jsonify(all_products)

# create new product
@app.route("/store/product/create", methods=["POST"])
def create_product():
    data = request.json
    try:
        name = data.get("name")
        store = data.get("storeId")
        brand = data.get("brand")
        productExist = Product.query.filter_by(
            name=name, store=store, brand=brand).first()

        if productExist:
            return jsonify(
                success=False,
                error="This product is alrealy exist"
            )
        else:
            description = data.get("description")
            price = data.get("price")
            quantity = data.get("quantity")
            types = data.get("types")
            source = data.get("source")

            try:
                imagesName = f"{len(os.listdir('./images/products'))}.jpg"
                imagesFile = request.files["photo"]
                imagesFile.save(f"./images/products/{imagesName}")
            except:
                imagesName = "product/default.jpg"

            newProduct = Product(
                name, description, price, quantity, store, imagesName, types, brand, source)

            try:
                db.session.add(newProduct)
                db.session.commit()

                return jsonify(
                    success=True,
                )

            except:
                return jsonify(
                    success=False,
                    error="cannot create this product"
                )
    except:
        return jsonify(
            success=False,
            error="cannot create this product"
        )

# delete product
@app.route("/store/product/delete", methods=["GET"])
def delete_product():
    productId = get_queries(request)["id"]

    try:
        product = Product.query.filter_by(id=productId)
        if not product:
            return jsonify(
                success=False,
                error="Cannot find this product"
            )
        product.delete()
        db.session.commit()

        return jsonify(
            success=True
        )
    except:
        return jsonify(
            success=False,
            error="Cannot delete this product"
        )

# update product
@app.route("/store/product/update", methods=["POST"])
def update_product():
    data = request.json
    try:
        id = data.get("id")
        product = Product.query.filter_by(id=id).first()
        if product:
            name = data.get("name")
            description = data.get("description")
            price = data.get("price")
            quantity = data.get("quantity")

            try:
                product.name = name
                product.description = description
                product.price = price
                product.quantity = quantity
                db.session.commit()

                return jsonify(
                    success=True
                )
            except:
                return jsonify(
                    success=False,
                    error="Cannot update this product"
                )
        else:
            return jsonify(
                success=False,
                error="Product not found"
            )
    except:
        return jsonify(
            success=False,
            error="Cannot update this product!"
        )

# BILL API
@app.route("/store/bill/create", methods=["POST"])
def create_bill():
    rs = []
    data = request.json
    userId = data.get("userId")
    address = data.get("address")
    lx = data.get("lx")
    ly = data.get("ly")
    phone = data.get("phone")
    products = data.get("products")
    # products = products.split(",")
    numberStoreProduct = dict()

    for product in products:
        storeId = Product.query.filter_by(id=int(list(product.keys())[0])).first().store
        
        numberStoreProduct[storeId] = numberStoreProduct.get(
            storeId, list()) + [product]

    for store, items in numberStoreProduct.items():
        storeId = int(store)
        totalPrice = 0
        for item in items:
            pId = list(item.keys())[0]
            quantity = int(item.get(pId))
            pId = int(pId)
            
            p = Product.query.filter_by(id=pId).first()
            price = float(p.price)

            totalPrice += price * quantity
        
        try:
            newBill = Bill(userId, storeId, str(
                totalPrice), lx, ly, address, phone)
            db.session.add(newBill)
            db.session.commit()
            billId = billsSchema.dump(Bill.query.all())[-1]["id"]
            rs.append(f'#{billId}')
            for item in items:
                pId = list(item.keys())[0]
                quantity = int(item.get(pId))
                pId = int(pId)
                newBillDetail = Bill_detail(billId, pId, quantity)
                db.session.add(newBillDetail)
                db.session.commit()

        except:
            return jsonify(
                success=False,
                error="cannot create bill"
            )
    return jsonify(
        success=True,
        billId= " &".join(rs)
    )

# get bill
@app.route("/store/bill/getBills", methods=["GET"])
def get_all_bill():
    queries = get_queries(request)
    print(queries)
    try:
        all_bill = format_bills_list(filter_arr_by_queries(
            billsSchema.dump(Bill.query.all()), queries))
        return jsonify(all_bill)

    except:
        return jsonify(
            success=False,
            error="cannot show bill list"
        )

# update bill by id
@app.route("/store/bill/update", methods = ["POST"])
def update_bill():
    data = request.json
    try:
        bill = Bill.query.filter_by(id = data.get("id")).first()
        bill.isCheck = data.get("check")
        db.session.commit()

        return jsonify(
            success = True
        )
    except:
        return jsonify(
            success = False,
            error = "cannot updata"
        )

##POST API
# location
@app.route("/location", methods=["GET"])
def location():
    queries = get_queries(request)
    posts = Post.query.all()
    all_posts = format_posts_list(
        filter_arr_by_queries(postsSchema.dump(posts), queries))

    return jsonify(all_posts)

##POST Diagotic
# diaglogic
@app.route("/diaglogic", methods=["POST"])
def diaglogic():
    chickenList = ["cock", "hen", "chicken", "bird", "quail", "partridge", "pillow"]

    isCorrect = True
    # load a single image
    name = f'{len(Post.query.all())+1}.jpg'
    photo = request.files["photo"]
    photo.save(f'E:/dev/chicken-app/api/server/images/data/{name}')
    
    print(f"image has saved with name {name}")

    img = image.load_img(f'E:/dev/chicken-app/api/server/images/data/{name}', target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

        # check prediction
    predRs = checkChicken.predict(x)
    predCheck = decode_predictions(predRs, top=3)[0]
    print(predCheck)
    check = False
    for i in predCheck:
        if i[1] in chickenList: 
            check = True
            break


    if check == False:
        res = {"success": False, "mgs": "Vui lòng chụp ảnh rõ hơn hoặc gần đối tượng để có được kết quả chính xác. Xin cám ơn!"}
        return jsonify(res)

    new_image = load_image(f'E:/dev/chicken-app/api/server/images/data/{name}', 64)

    # check prediction
    pred = model.predict(new_image)
    print("Thong so cac benh:", pred)
    rs = max(pred[0])
    if rs < 90:
        isCorrect = False
    pred = pred[0]
    pred = pred.tolist()
    idx = pred.index(rs)
    print("Result is:", idx)
    result = Sickness.query.filter_by(id=(idx + 1)).first()

    newPost = Post(int(idx+1), name, float(request.values["lng"]), float(
        request.values["lat"]), int(request.values["userId"]))

    userAddress = User.query.filter_by(
        id=int(request.values["userId"])).first().address

    print("user address is:", userAddress)

    department = Department.query.filter_by(name=userAddress).first()
    if department: phonenumber = department.phonenumber
    else: phonenumber = "không có cơ sở nào gần đây"
    

    try:

        db.session.add(newPost)
        db.session.commit()
        print("new port has saved to server")

    except:
        return jsonify(
            success=False,
            error="cannot post"
        )

    res = {"success": True, "sickness": result.name, "description": result.description,
           "solution": result.solution, "isCorrect": isCorrect, "Department": phonenumber}

    return jsonify(res)

##WEB SERVER
# home
@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/user")
def home_user():
    return render_template("user.html")

@app.route("/chart")
def home_chart():
    return render_template("chart.html")

#map
@app.route("/maps")
def maps_page():
    return render_template("map.html")

#chat
@app.route("/chat")
def chat_page():
    return render_template("chat.html")