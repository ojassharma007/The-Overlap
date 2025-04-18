from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('leagues/', views.leagues, name='leagues'),
    path('alleagues/', views.all_leagues, name='all_leagues'),
    path('fixtures/', views.fixtures, name='fixtures'),
    path('standings/', views.standings, name='standings'),
    path('teams/', views.teams, name='teams'),
    path('stats/', views.stats, name='stats'),
    path('live_fixtures/', views.live_fixtures, name='live_fixtures'),
    path("fixture_details/", views.fixture_details, name="fixture_details"),
    path("players/", views.players, name="players"),
    path("lineup/", views.lineup, name="lineup"),
    path("events/", views.events, name="events"),
    path("fixture_stats/", views.fixture_stats, name="fixture_stats"),
    path("player_profile/", views.player_profile, name="player_profile"),
    
    path("__reload__/", include("django_browser_reload.urls")),

]
