from server.models import User, Post, Product, Bill, Bill_detail, usersSchema, postsSchema, productSchema, productsSchema, billsSchema, billDetailsSchema
from urllib import parse
from keras.preprocessing import image
import numpy as np

def get_queries(request):
    return dict(parse.parse_qsl(parse.urlsplit(request.url).query))

def filter_arr_by_queries(arr, queries):
    def filter_by_query(item):
        rs = True
        for key, value in queries.items():
            rs = rs and (str(item[key]) == value)
        return rs
    
    listFilter = list(filter(filter_by_query, arr))
    return listFilter

def format_products_list(arr):
    res = []
    for product in arr:
        feature = {
            "id": str(product["id"]),
            "storeName": User.query.filter_by(id = product["store"]).first().username,
            "name": product["name"],
            "description": product["description"],
            "price": product["price"],
            "quantity": product["quantity"],
            "images": product["images"],
            "types": product["types"],
            "brand": product["brand"],
            "source": product["source"]
        }

        res.append(feature)
    
    return res

def format_bills_list(arr):
    def maps_bill_details(item):
        try:
            product = Product.query.filter_by(id = item["pId"]).first()
            product.quantity = item["quantity"]
            product = productSchema.dump(product)
            return product
        except:
            pass
    

    res = []
    for bill in arr:
        username = User.query.filter_by(id = int(bill["userId"])).first().username

        bill_detail = Bill_detail.query.filter_by(bId = int(bill["id"]))
        bill_detail = billDetailsSchema.dump(bill_detail)
        
        bill_detail = list(map(maps_bill_details, bill_detail))

        feature = {
            "id": bill["id"],
            "username": username,
            "storeId": bill["storeId"],
            "products": bill_detail,
            "total_price": bill["totalPrice"],
            "address": bill["address"],
            "phonenumber": bill["phone"],
            "status": bill["status"],
            "date": str(bill["date_register"])
        }

        res.append(feature)
    return res

def format_users_list(arr):
    res = []
    for user in arr:
        features = {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "phonenumber": user["phonenumber"],
            "address": user["address"],
            "code": user["code"],
            "date_register": str(user["date_register"])
        }

        res.append(features)
    return res

def format_posts_list(arr):
    res = []
    for post in arr:
        feature = {
            "sicknessId": str(post["sicknessId"]), 
            "cotinate": [
                post["lx"], 
                post["ly"]],
            "postPerson": format_users_list(usersSchema.dump(User.query.filter_by(id=post["user_id"])))[0]
        }
        res.append(feature)

    return res

def load_image(img_path, size, show=False):

    img = image.load_img(img_path, target_size=(size, size))
    img_tensor = image.img_to_array(img)
    # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    # imshow expects values in the range [0, 1]
    img_tensor /= 255.

    return img_tensor
