from django.conf.urls import url, include, patterns
from rest_framework.routers import SimpleRouter

from todo.api.resources import TodoViewSet, done

router = SimpleRouter()
router.register(r'todos', viewset=TodoViewSet)

urlpatterns = patterns(
    '',
    url(r'', include(router.urls)),
    url(r'^todos/(?P<pk>[^/.]+)/done/$', done, name='todo-done')
)
