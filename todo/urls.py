from django.urls import path
from .views import List_Detail, Task_Detail, Task_List, List_Not_Complete_List, List_List, List_Complete_List
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('list_nc/', List_Not_Complete_List.as_view(), name='list-list'), # Direct to not complete tasks (showing only non complete tasks)
    path('list_c/', List_Complete_List.as_view(), name='list-list'),  # Direct to complete tasks (showing all tasks)

    path('list_all/', List_List.as_view(), name='list-list'),# Direct to all list (showing all tasks)
    path('list_all/<slug:slug>/', List_Detail.as_view(), name='list-detail'),


    path('task/', Task_List.as_view(), name='task-list'), #Showing all tasks (Complete and non Complete
    path('task/<slug:slug>/', Task_Detail.as_view(), name='task-detail'), #Showing a specific tasks according to the slug

]
#Ability to retrieve Json and HTML views
urlpatterns = format_suffix_patterns(urlpatterns)
