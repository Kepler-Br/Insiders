from django.shortcuts import redirect

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)


# from django.shortcuts import get_object_or_404
# Create your views here.


class RootAddress(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("user_home", request.user.username)
        else:
            return redirect("login_page")
