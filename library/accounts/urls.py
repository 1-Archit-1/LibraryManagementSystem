
from django.urls import path, include
from .api import MemRegisterApi,LibRegisterApi,AddMember,Viewmembers,RemoveMembers,UpdateMember
urlpatterns = [
      path('api/lib-register', LibRegisterApi.as_view()),
      path('api/mem-register', MemRegisterApi.as_view()),
      path('api/add-member', AddMember.as_view()),
      path('api/view-member', Viewmembers.as_view()),
      path('api/remove-member', RemoveMembers.as_view()),
      path('api/update-member', UpdateMember.as_view())
]