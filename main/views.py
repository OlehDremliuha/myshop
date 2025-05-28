from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product

def getMain(request):
    return render(request, "main/index.html")

def logIn(request):

    if request.method == "POST":

        userName=request.POST['userName']
        userPassword=request.POST['userPass']

        user = authenticate(request, username=userName, password=userPassword)

        if user is not None:
            login(request, user)
            return redirect('main')
    
        return render(request, 'main/formLogIn.html', {'error': "Data is not correct"})

    return render(request, 'main/formLogIn.html')


def logUp(request):

    if request.method == "POST":

        userName=request.POST['userName']
        userPassword=request.POST['userPass']
        userPassword2=request.POST['userPass2']

        if userPassword == userPassword2:

            user = User.objects.create_user(userName, '', userPassword)
            user.save()

            user = authenticate(request, username=userName, password=userPassword)

            if user is not None:
                login(request, user)
            return redirect('main')
        
        return render(request, 'main/formLogUp.html', {'error': "Passwords are different"})


    return render(request, 'main/formLogUp.html')

@login_required
def logOut(request):
    logout(request)
    return redirect('main')



@login_required
def addProduct(request):

    if request.method == "POST":

        name = request.POST['name']
        description = request.POST['description']
        try:
            price = float(request.POST['price'])
        except:
            return render(request, 'main/addProductForm.html', {'error': 'Price must be number'})
        try:
            img = request.FILES['img']
        except:
            return render(request, 'main/addProductForm.html', {'error': 'File problem'})
        
        product = Product(name=name, description=description, price=price, img=img)
        product.save()

        return redirect('main')
        

    return render(request, 'main/addProductForm.html')


def shop(request):

    products = Product.objects.all()
    
    return render(request, 'main/shop.html', {"products": products})


#Реалізувати Авторизацію та регістрацію