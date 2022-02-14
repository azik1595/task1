from  api import views
routes = [
      ('POST', '/api/v1/users/registration/', views.registration),
      ('POST', '/api/v1/users/login/', views.login),
      ('GET', '/api/v1/event/list/', views.events_list),
      ('POST', '/api/v1/event/new/', views.events_new)
]