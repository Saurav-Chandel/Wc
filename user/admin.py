from django.contrib import admin
from .models import User,Profile,Post,Category,Comments,Reply,UserFollowing,UserNotifications,CommentSettings,LikeSettings,ShareSettings
# Register your models here.

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id','post', 'user', 'comment','like','created_at')
  

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserFollowing)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comments,CommentsAdmin)
admin.site.register(Reply)
admin.site.register(UserNotifications)
admin.site.register(CommentSettings)
admin.site.register(LikeSettings)
admin.site.register(ShareSettings)



