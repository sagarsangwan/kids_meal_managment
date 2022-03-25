from django.shortcuts import render


# Create your views here.
def home(request):

    return render(request, 'pages/home.html')


def signup(request):
    print(request)
    if request.method == 'POST':
        print(request)
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        confirm_password = request.POST['confirm_password']
        print(user_name, user_email, user_password, confirm_password)

    return render(request, 'pages/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # if user is not None:
        #     login(request, user)
        #     return redirect('home')
        # else:
        #     return redirect('login')
    return render(request, 'pages/login.html')
