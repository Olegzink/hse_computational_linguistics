from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
	# main page
	path('', views.index, name='index'),
	path('reviews/all/', views.reviews, name='reviews'),
	# for filtering /reviews/all/positive or /reviews/all/negative
	path('reviews/all/<str:sentiment>', views.reviews, name='reviews'),
	path('reviews/<int:review_id>/', views.current_review, name='current_review'),
	path('aspects/all/', views.aspects_all, name='aspects_all'),
	path('aspects/negative/', views.aspects_negative, name='aspects_negative'),
	path('aspects/negative/<str:aspect>/', views.aspects_negative_by_aspect, name='aspects_negative_by_aspect'),
	path('aspects/<str:aspect>/', views.reviews_by_aspects, name='reviews_by_aspects'),
	path('intentions/all/', views.intentions_all, name='intentions_all'),
	path('intentions/positive/', views.intentions_positive, name='intentions_positive'),
	path('intentions/negative/', views.intentions_negative, name='intentions_negative'),
]