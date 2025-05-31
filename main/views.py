from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product, Comment, Basket, ProductBasket
import datetime
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
import math

userId = None
currentPage = 1
countBlock = 4

def getMain(request):
    return render(request, "main/index.html")

def logIn(request):

    global userId

    if request.method == "POST":

        userName=request.POST['userName']
        userPassword=request.POST['userPass']

        user = authenticate(request, username=userName, password=userPassword)
        userId = user.id

        if user is not None:
            login(request, user)
            return redirect('main')
    
        return render(request, 'main/formLogIn.html', {'error': "Data is not correct"})

    return render(request, 'main/formLogIn.html')


def logUp(request):

    global userId

    if request.method == "POST":

        userName=request.POST['userName']
        userPassword=request.POST['userPass']
        userPassword2=request.POST['userPass2']

        if userPassword == userPassword2:

            user = User.objects.create_user(userName, '', userPassword)
            user.save()

            user = authenticate(request, username=userName, password=userPassword)

            userId = user.id

            if user is not None:
                login(request, user)
            return redirect('main')
        
        return render(request, 'main/formLogUp.html', {'error': "Passwords are different"})


    return render(request, 'main/formLogUp.html')

@login_required
def logOut(request):

    global userId
    userId = None
    logout(request)
    return redirect('main')



@login_required
def addProduct(request):

    if request.user.is_staff:

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
    
    else:

        return redirect('main')


def shop(request, page):

    global currentPage
    global countBlock

    currentPage = page

    count = Product.objects.all().count()
    if (count/countBlock > 1):
        pages = []
        for item in range(math.ceil(count/countBlock)):
            pages.append({"number": item + 1, "url": "shop/" + str(item + 1)})
    

    products = Product.objects.all()[countBlock * (currentPage-1):countBlock * currentPage]
    return render(request, 'main/shop.html', {"products": products, "pages": pages})


def getProduct(request, id):

    product = Product.objects.filter(id=id).first()
    comments = Comment.objects.filter(productId=product).order_by('-date')

    return render(request, 'main/product.html', {"product": product, "comments": comments})


@login_required
def addComent(request, id):

    global userId
    prod = Product.objects.filter(id=id).first()
    userObj = User.objects.filter(id=userId).first()
    comentText = request.POST["comentText"]
    date = datetime.datetime.now()

    coment = Comment(productId=prod, userId=userObj, comentText=comentText, date=date)
    coment.save()

    return redirect("product", id)




def getProfile(request, id):

    userProfile = User.objects.get(id=id)

    return render(request, 'main/profile.html', {"userProfile": userProfile})


@login_required
def editProfile(request, id):

    userProfile = User.objects.get(id=id)

    if request.method == "POST":

        if ("username" in request.POST.keys()):

            userName = request.POST["username"]
            userProfile.username=userName
            userProfile.save()
            return redirect("profile", id)

        if ("email" in request.POST.keys()):

            userEmail = request.POST["email"]
            userProfile.email=userEmail
            userProfile.save()
            return redirect("profile", id)
        

        if ("password" in request.POST.keys()):

            userPass = request.POST["password"]
            userPass2 = request.POST["password2"]
            if userPass == userPass2:
                userProfile.set_password(userPass)
                userProfile.save()
                login(request, userProfile)
                return redirect("profile", id)
            else:
                error = "Password is not confirm"
                return render(request, 'main/editPage.html', {"userProfile": userProfile, "error": error})
        

    userProfile = User.objects.get(id=id)

    return render(request, 'main/editPage.html', {"userProfile": userProfile})



@login_required
def getBasket(request, id):

    user = User.objects.get(id=id)

    try:
        basket = Basket.objects.get(userId=user)
        products = ProductBasket.objects.filter(basketId=basket)
        totalPrice = 0
        for item in products:
            totalPrice+=item.productId.price
        return render(request, 'main/userBasket.html', {"products": products, "basketId": basket.id, "totalPrice": totalPrice})
    except:
        warning = "No one product in your basket"
        return render(request, 'main/userBasket.html', {"warning": warning})


@login_required
def addToBasket(request, id):
    
    user = User.objects.get(id=userId)

    try: 

        basket = Basket.objects.get(userId=user)

    except:

        basket = Basket(userId=user)
        basket.save()

    product = Product.objects.get(id=id)
     
    count = ProductBasket.objects.filter(basketId=basket, productId=product).count()

    if count >= 1:

        comments = Comment.objects.filter(productId=product).order_by('-date')
        return render(request, 'main/product.html', {"product": product, "comments": comments, "error": True})

    else:
        productBasket = ProductBasket(basketId=basket, productId=product)
        productBasket.save()

    return redirect('product', id)

@login_required
def deleteProductBasket(request, basketId, productId):


    basket = Basket.objects.get(id=basketId)
    product = Product.objects.get(id=productId)
    productBasket = ProductBasket.objects.get(basketId=basket, productId=product)
    productBasket.delete()

    products = ProductBasket.objects.filter(basketId=basket)
    return redirect('userBasket', basketId)


@login_required
def pay(request, basketId):

    basket = Basket.objects.get(id=basketId)
    basket.delete()

    return redirect('main')





class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'main/password_reset.html'
    email_template_name = 'main/password_reset_email.html'
    subject_template_name = 'main/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('main')






#Реалізувати Авторизацію та регістрацію