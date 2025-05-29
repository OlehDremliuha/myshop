from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import Product, Comment
import datetime
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

userId = None

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


def shop(request):

    products = Product.objects.all()
    
    return render(request, 'main/shop.html', {"products": products})


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