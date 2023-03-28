from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetails, PostCreate, PostEdit, PostDelete


urlpatterns = [

   path('', PostDetails.as_view(), name='post_detail'),
   path('edit/', PostEdit.as_view(), name='news_edit'),
   path('delete/', PostDelete.as_view(), name='news_delete'),

]
