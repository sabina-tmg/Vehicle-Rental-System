from .models import Category
from datetime import datetime

def all_categories(request):
    categories = Category.objects.all()
    date = datetime.now().year
    return {'categories': categories,'date':date,}