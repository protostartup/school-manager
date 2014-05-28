from django.conf.urls import patterns, include, url
from schools.views import (
    SchoolList, SchoolDetail, SchoolCreate, SchoolUpdate, SchoolDelete, 
    LocationList, LocationDetail, LocationCreate, LocationUpdate, LocationDelete,
    CourseList, CourseCreate, CourseUpdate, CourseDelete, CourseDetail,
    StudentCreate, StudentList,
    InstructorCreate, InstructorList,
    UserDetail, UserUpdate,
    register, home
)
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from schools.models import School

urlpatterns = patterns('',
    url(r'^$', login_required(home)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/register/$', register),
    url(r'^analytics/', include('analytics.urls')),

    #School resources
    url(r'^schools/$', SchoolList.as_view(), name='school_list'),
    url(r'^schools/(?P<pk>\d+)/$', SchoolDetail.as_view(), name='school_detail'),
    url(r'^schools/create/$', SchoolCreate.as_view(success_url='/schools/'), name='school_create'),
    url(r'^schools/(?P<pk>\d+)/update/$', SchoolUpdate.as_view(success_url='/schools/'), name='school_update'),
    url(r'^schools/(?P<pk>\d+)/delete/$', SchoolDelete.as_view(success_url='/schools/'), name='school_delete'),

    #Location resources
    url(r'^schools/(?P<school_id>\d+)/locations/$', LocationList.as_view(), name='location_list'),
    url(r'^locations/(?P<pk>\d+)/$', LocationDetail.as_view(), name='location_detail'),
    url(r'^schools/(?P<school_id>\d+)/locations/create/$', LocationCreate.as_view(), name='location_create'),
    url(r'^locations/(?P<pk>\d+)/update/$', LocationUpdate.as_view(), name='location_update'),
    url(r'^locations/(?P<pk>\d+)/delete/$', LocationDelete.as_view(), name='location_delete'),

    #Course resources
    url(r'^locations/(?P<location_id>\d+)/courses/$', CourseList.as_view(), name='course_list'),
    url(r'^courses/(?P<pk>\d+)/$', CourseDetail.as_view(), name='course_detail'),
    url(r'^locations/(?P<location_id>\d+)/courses/create/$', CourseCreate.as_view(), name='course_create'),
    url(r'^courses/(?P<pk>\d+)/update/$', CourseUpdate.as_view(), name='course_update'),
    url(r'^courses/(?P<pk>\d+)/delete/$', CourseDelete.as_view(), name='course_delete'),

    #User Resources
    url(r'^schools/(?P<school_id>\d+)/students/$', StudentList.as_view(), name='student_list'),
    url(r'^schools/(?P<school_id>\d+)/students/create/$', StudentCreate.as_view(), name='student_create'),
    url(r'^schools/(?P<school_id>\d+)/instructors/$', InstructorList.as_view(), name='instructor_list'),
    url(r'^schools/(?P<school_id>\d+)/instructors/create/$', InstructorCreate.as_view(), name='instructor_create'),
    url(r'^users/(?P<username>\w+)/$', UserDetail.as_view(), name='user_view'),
    url(r'^users/(?P<username>\w+)/update/$', UserUpdate.as_view(), name='user_update'),
)

#URL routes for API
from rest_framework import routers
from api.views import (
    SchoolViewSet, LocationViewSet, UserViewSet, StudentViewSet, InstructorViewSet, GroupViewSet, CourseViewSet,
    )
from django.conf.urls import patterns, url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'instructors', InstructorViewSet, base_name='instructors')
router.register(r'students', StudentViewSet, base_name='students')
router.register(r'groups', GroupViewSet)
router.register(r'schools', SchoolViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'courses', CourseViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns += (
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
