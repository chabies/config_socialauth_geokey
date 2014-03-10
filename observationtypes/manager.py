from django.db import models
from django.core.exceptions import PermissionDenied

from model_utils.managers import InheritanceManager

from projects.models import Project

from .base import STATUS


class ActiveMixin(object):
    def active(self, *args, **kwargs):
        return self.get_query_set().filter(status=STATUS.active)


class ObservationTypeManager(ActiveMixin, models.Manager):
    def active(self, *args, **kwargs):
        return self.get_query_set().filter(status=STATUS.active)

    def get_list(self, user, project_id):
        """
        Returns all observationtype objects the user is allowed to access
        """
        project = Project.objects.get_single(user, project_id)
        if (project.is_admin(user)):
            return project.observationtypes.all()
        else:
            return project.observationtypes.active()

    def get_single(self, user, project_id, observationtype_id):
        """
        Returns all a single observationtype. Raises PermissionDenied if user
        is not eligable to access the observationtype.
        """
        observation_type = Project.objects.get_single(
            user, project_id).observationtypes.get(pk=observationtype_id)

        if (observation_type.status == STATUS.active or
                observation_type.project.is_admin(user)):
            return observation_type
        else:
            raise PermissionDenied('You are not allowed to access this '
                                   'observationtype')

    def as_admin(self, user, project_id, observationtype_id):
        """
        Returns all a single observationtype for an project admin.
        """
        return Project.objects.as_admin(
            user, project_id
            ).observationtypes.get(pk=observationtype_id)


class FieldManager(ActiveMixin, InheritanceManager):
    use_for_related_fields = True

    def all(self):
        return self.get_query_set().select_subclasses()

    def get_list(self, user, project_id, observationtype_id):
        """
        Returns all fields the user is allowed to access.
        """
        project = Project.objects.get_single(user, project_id)

        if project.is_admin(user):
            return project.observationtypes.get(
                pk=observationtype_id).fields.all().select_subclasses()
        else:
            observationtype = project.observationtypes.get(
                pk=observationtype_id)
            if observationtype.status == STATUS.active:
                return observationtype.fields.active().select_subclasses()

    def get_single(self, user, project_id, observationtype_id, field_id):
        """
        Return a single field
        """
        project = Project.objects.get_single(user, project_id)
        observationtype = project.observationtypes.get(pk=observationtype_id)
        field = observationtype.fields.get_subclass(pk=field_id)

        if project.is_admin(user):
            return field
        else:
            if observationtype.status == STATUS.active:
                if field.status == STATUS.active:
                    return field
                else:
                    raise PermissionDenied('You are not allowed to access '
                                           'this field')
            else:
                raise PermissionDenied('You are not allowed to access this '
                                       'observationtype')

    def as_admin(self, user, project_id, observationtype_id, field_id):
        """
        Returns all a single field for an project admin.
        """
        return Project.objects.as_admin(
            user, project_id).observationtypes.get(
            pk=observationtype_id).fields.get_subclass(pk=field_id)


class LookupQuerySet(models.query.QuerySet):
    """
    QuerySet for models having a field status. User by ActiveManager.
    """
    def active(self):
        return self.filter(status=STATUS.active)


class LookupValueManager(models.Manager):
    """
    Manager for models having a field status. Is required to render active
    items only in templates.
    """
    use_for_related_fields = True

    def get_query_set(self):
        return LookupQuerySet(self.model)

    def active(self, *args, **kwargs):
        return self.get_query_set().active(*args, **kwargs)
