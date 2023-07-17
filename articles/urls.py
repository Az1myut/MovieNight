from django.urls import path
from .views import(
     ShowArticlesListView,
     ShowArticleDetailView,
     ArticleDeleteView,
     ArticleUpdateView,
     ArticleCreateView,
     ArticleCommentDeleteView,
     ArticleAddChildCommentCreateView,
)
app_name = 'articles'
urlpatterns = [
    path('create',ArticleCreateView.as_view(), name='article_create'),
    path('<slug:slug>',ShowArticleDetailView.as_view(), name='article_detail'),
    path('<slug:slug>/delete',ArticleDeleteView.as_view(), name='article_delete'),
    path('<slug:slug>/update',ArticleUpdateView.as_view(), name='article_update'),
    path('<slug:slug>/comments/<uuid:comment_id>/add',ArticleAddChildCommentCreateView.as_view(), name='article_comment_child_add'),
    path('<slug:slug>/comments/<uuid:comment_id>/delete',ArticleCommentDeleteView.as_view(), name='article_comment_delete'),
    path('',ShowArticlesListView.as_view(), name='articles_list'),


    
]