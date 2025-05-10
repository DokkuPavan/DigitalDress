# views.py
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
import json, random
import os

# Create your views here.

def home(request):
    # Load clothes data
    clothes_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'clothes_data.json')
    with open(clothes_data_path, 'r') as file:
        temp = json.load(file)
    clothes_data = temp['clothes']
    random.shuffle(clothes_data)
    content = {
        "clothes_data": clothes_data,
    }
    return render(request, 'index.html', context=content)

def user_authenticate(username, password):
    # Use relative path for user data file
    user_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'user_data.json')
    with open(user_data_path, 'r') as file:
        data = json.load(file)
        for user in data['users']:
            if user['email'] == username and user['password'] == password:
                return user['id']
        return None

flag = None
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email', None)
        password = request.POST.get('password', None)
        user = user_authenticate(username=username, password=password)
        if user is not None:
            # Store user ID in session
            request.session['user_id'] = user
            # Redirect to a success page or homepage
            return redirect('home')
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def user_signup(request):
    if request.method == 'POST':
        # Use relative path for user data file
        user_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'user_data.json')
        with open(user_data_path, 'r+') as file:
            users = json.load(file)
            new_user = {
                "id": str(len(users["users"]) + 1),
                "name": request.POST.get('name', None),
                "email": request.POST.get('email', None),
                "password": request.POST.get('password', None),
                "cart": []
            }
            users["users"].append(new_user)
            file.seek(0)
            json.dump(users, file, indent=4)
        return redirect('login')
    return render(request, 'signup.html')

def shop(request):
    clothes_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'clothes_data.json')
    with open(clothes_data_path, 'r') as file:
        temp = json.load(file)
    clothes_data = temp['clothes']
    content = {
        "clothes_data": clothes_data,
    }
    return render(request, 'shop.html', content)

def store_image_url(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_url = data.get('image_url')
        if image_url:
            global_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'global_data.json')
            with open(global_data_path, 'r+') as file:
                json_data = json.load(file)
                json_data['data'][0]['image_url'] = image_url
                file.seek(0)
                json.dump(json_data, file, indent=4)
            return JsonResponse({'message': 'Image URL stored successfully'})
    return JsonResponse({'error': 'Failed to store image URL'}, status=400)

def product_details(request):
    return render(request, 'product-details.html')

def profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'user_data.json')
        with open(user_data_path, 'r') as file:
            user_data = json.load(file)
            for user in user_data['users']:
                if user['id'] == user_id:
                    user_details = user
                    break
        clothes_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'clothes_data.json')
        with open(clothes_data_path, 'r') as clothes_file:
            clothes_data = json.load(clothes_file)
        orders_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'orders.json')
        with open(orders_data_path, 'r') as orders_file:
            orders_data = json.load(orders_file)
            user_orders = [order for order in orders_data['orders'] if order['user_id'] == user_id]
            user_order_items = []
            for order in user_orders:
                order_items = []
                for item in clothes_data['clothes']:
                    if item['id'] == order['clothes_id']:
                        order_items.append(item)
                user_order_items.append({
                    'id': order['id'],
                    'transaction_date': order['transaction_date'],
                    'total_amount': order['total_amount'],
                    'items': order_items
                })
    else:
        user_details = None
        clothes_data = None
        user_order_items = None
    
    return render(request, 'profile.html', {'user_details': user_details, 'clothes_data': clothes_data, 'user_order_items': user_order_items})

def check_out(request):
    try:
        if request.session['user_id'] is not None:
            print('session name : ', request.session['user_id'])
    except(KeyError):  # If session is empty
        return HttpResponse("<h2> Login to continue ... </h2>")
    return render(request, 'checkout.html')

def contact(request):
    return render(request, 'contact.html')

def make_dir():
    os.system("cd /content/ && mkdir inputs && cd inputs && mkdir test && cd test && mkdir cloth cloth-mask image image-parse openpose-img openpose-json")

def trail(request):
    output_image_path = None
    if request.method == 'POST':
        # Get the uploaded images
        user_image = str(request.FILES.get('image1'))
        cloth_image = str(request.FILES.get('image2'))

        output_image_path = '/static/img/res/' + cloth_image[cloth_image.find('.')-1] + user_image[0] + '.png'
        
        # get absolute path of user and cloth images
        user_image = '/static/img/human/' + user_image
        cloth_image = '/static/img/product/' + cloth_image

        print('o/p: ', output_image_path)

        # Pass output_image_path to the template context
        context = {
            'output_image_path': output_image_path,
            'user_image': user_image,
            'cloth_image': cloth_image
        }
        if flag is not None:
            make_dir()

            # Save the images to the desired locations
            model_image_path = '/content/inputs/test/image/model.jpg'
            cloth_image_path = '/content/inputs/test/image/cloth.jpg'

            save_image(user_image, model_image_path)
            save_image(cloth_image, cloth_image_path)

            # Call the run method here
            # run(Image.open(model_image_path), Image.open(cloth_image_path))
            os.system("python /content/clothes-virtual-try-on/run.py")

            op = os.listdir("/content/output")[0]
            output_image_path = f"/content/output/{op}"

            # Pass the output image path to the template context
            context = {'output_image_path': output_image_path}

        return render(request, 'trail_room_res.html', context)

    return render(request, 'trail_room.html')

# Reset btn
def trail_res(request):
    return render(request, 'trail_room.html')

def save_image(image_file, save_path):
    with open(save_path, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

def trail1(request, image_id):
    clothes_data_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'clothes_data.json')
    with open(clothes_data_path, 'r') as file:
        temp = json.load(file)
    clothes_data = temp['clothes']
    image_url, output_image = None, None
    for item in clothes_data:
        if int(item['id']) == int(image_id):
            image_url = item['image_url']
            break
    content = {
        'image_url_dict': image_url,
        'output_image_path': output_image
    }
    print(content['image_url_dict'])

    return render(request, 'trail_room1.html', content)
