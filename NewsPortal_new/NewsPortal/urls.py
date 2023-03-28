from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetails, PostCreate, PostEdit, PostDelete


urlpatterns = [

   path('', PostList.as_view()),
   path('<int:pk>', PostDetails.as_view(), name='post_detail'),
   path('search/', PostList.as_view(), name='post_list'),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', PostEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),

]
