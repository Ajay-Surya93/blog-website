from django.core.management.base import BaseCommand
from blog.models import Category
from typing import Any

class Command(BaseCommand):
    help = "This commands inserts Category data"
    
    def handle(self, *args:Any, **options:Any):
        Category.objects.all().delete()
        
        categories = ['Sports',"Science","Technology","Arts","Food"]

        for category_name in categories:
            Category.objects.create(name=category_name)
        
        self.stdout.write(self.style.SUCCESS("Completed inserting Data"))