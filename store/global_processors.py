from .models import Category

#Global Processors
def navbar_categories(request):
  categories = Category.objects.all()
  return {'categories': categories}