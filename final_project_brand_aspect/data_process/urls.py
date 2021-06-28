from django.urls import path
from . import views

app_name = 'data_process'

urlpatterns = [
    path('data_process/process_csv/', views.process_csv, name='process_csv'),
    path('data_process/process_phrases/', views.process_phrases, name='process_phrases'),
    path('data_process/submit_review/', views.submit_review, name='submit_review'),
    path('data_process/upload_thematic_tokens_to_db/<str:token_class>', views.upload_thematic_tokens_to_db, name='upload_thematic_tokens_to_db'),
    path('data_process/upload_sentiment_tokens_to_db/', views.upload_sentiment_tokens_to_db, name='upload_sentiment_tokens_to_db'),
]