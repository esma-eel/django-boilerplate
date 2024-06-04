from django.shortcuts import render


def dashboard(request):
    context = {
        "menu_item": "dashboard",
        "submenu_item": "dashboard",
    }
    return render(
        request=request,
        template_name="dashboard/dashboard.html",
        context=context,
    )
