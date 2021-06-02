
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from user_service.forms import UserLoginForm

@csrf_exempt
def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/data-schemas')
        token = Token.objects.create(user=user)
        print(token.key)
    return render(request, "user_service/login.html", {'form': form})

def logout_user(request):
    logout(request)
    return redirect('/users/login/')
