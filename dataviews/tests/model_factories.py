import datetime
import factory

from projects.tests.model_factories import UserF, ProjectF

from ..models import View, ViewGroup


class ViewFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = View

    name = factory.Sequence(lambda n: 'name_%d' % n)
    description = factory.LazyAttribute(lambda o: '%s description' % o.name)
    creator = factory.SubFactory(UserF)
    created_at = datetime.date(2014, 11, 11)
    status = 'active'
    project = factory.SubFactory(ProjectF)


class ViewGroupFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ViewGroup

    name = factory.Sequence(lambda n: 'name_%d' % n)
    description = factory.LazyAttribute(lambda o: '%s description' % o.name)
    can_edit = False
    can_read = False
    can_view = True
    view = factory.SubFactory(ViewFactory)

    @factory.post_generation
    def add_users(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for user in extracted:
                self.users.add(user)
