from django.shortcuts import render

#Cart
def cart_summary(request):
    return render(request, "cart_summary.html", {})
def cart_add():
    pass
def cart_delete():
    pass
def cart_update():
    pass


