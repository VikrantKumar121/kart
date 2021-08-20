from .models import Category

def categories_list(self):
    """"""
    categories = Category.objects.all()
    context = {
        'categories_list': categories,
    }
    return context
