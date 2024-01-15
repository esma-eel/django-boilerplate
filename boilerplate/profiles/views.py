from django.shortcuts import render


# Create your views here.
def profile_home(request, username=None):
    return render(
        request,
        template_name="profiles/profile.html",
    )

def profile_view(request, username=None):
    return render(
        request,
        template_name="profiles/profile.html",
    )
