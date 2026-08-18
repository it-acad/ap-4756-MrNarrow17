from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

user_model = get_user_model()


@login_required
def user_list(request):
    users = user_model.objects.all()
    return render(request, "user/user_list.html", {"users": users})


@login_required
def user_info(request, id: int):
    user = user_model.objects.get(pk=id)
    return render(request, "user/user.html", {"user": user})
