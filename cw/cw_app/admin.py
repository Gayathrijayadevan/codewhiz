from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(QuizAttempt)
admin.site.register(UserAnswer)





