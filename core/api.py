from django.conf.urls import patterns, url

from projects import views as project_views
from observationtypes import views as observationtype_views
from contributions import views as contribution_views

urlpatterns = patterns(
    '',
    # ###########################
    # PROJECTS
    # ###########################
    url(
        r'^projects$',
        project_views.ProjectApiList.as_view(),
        name='project'),
    url(
        r'^projects/(?P<project_id>[0-9]+)$',
        project_views.ProjectApiSingle.as_view(),
        name='project_single'),

    # ###########################
    # OBSERVATIONS
    # ###########################

    url(
        r'^projects/(?P<project_id>[0-9]+)/observations$',
        contribution_views.Observations.as_view(),
        name='project_observations'),
    url(
        r'^projects/(?P<project_id>[0-9]+)/observations/(?P<observation_id>[0-9]+)$',
        contribution_views.SingleObservation.as_view(),
        name='project_single_observation'),

    # ###########################
    # LOCATIONS
    # ###########################

    url(
        r'^projects/(?P<project_id>[0-9]+)/locations$',
        contribution_views.Locations.as_view(),
        name='project_locations'),

    # ###########################
    # OBSERVATION TYPES
    # ###########################
    url(
        r'^projects/(?P<project_id>[0-9]+)/observationtypes/(?P<observationtype_id>[0-9]+)$',
        observationtype_views.ObservationTypeApiSingle.as_view(),
        name='project_observation_types'),
)