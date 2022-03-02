from django.contrib import admin
from .models import User,Profile,Post,Category,Comments,Reply
# Register your models here.

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'user', 'comment','like','created_at')
  


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(Reply)



