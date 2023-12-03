"""
This file contains the TestSetup class which is the basis for all test cases
"""
import random

from faker import Faker
from rest_framework.test import APITestCase

from user.models import User

faker = Faker()
global_password = faker.password()


class TestSetup(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixtures = []
        super(TestSetup, cls).setUpClass()

    def setUp(self, authenticate=True):
        self.global_password = global_password
        if authenticate:
            self.user = generate_user()
            self.client.force_authenticate(user=self.user)


def generate_user(quantity=1, is_staff=None) -> User:
    objs = []
    for _ in range(quantity):
        data = create_fake_data_by_model(User)

        if is_staff is not None:
            data["is_staff"] = is_staff

        obj = User.objects.create(**data)
        objs.append(obj)

    return objs if len(objs) > 1 else objs[0]


def create_fake_data_by_model(model, auto_add=False, **kwargs):  # noqa: C901
    """
    Generate fake data based on a model
    """
    try:
        generic_exclude_fields = [
            "id",
            "is_superuser",
            "is_staff",
            "is_active",
            "created_by",
            "status",
            "last_login",
            "deleted_at",
            "created_at",
            "updated_at",
        ]

        data = {}
        for field in model._meta.fields:
            field_name = field.name
            model_name = model._meta.model_name
            is_nullable = field.null
            is_related = field.is_relation
            is_related_many = is_related and field.many_to_many
            max_size = field.max_length
            choices = field.choices

            type = field.get_internal_type()

            # If a getter exists for this field, it is used
            getter = "get_" + model_name + "_" + field_name
            if getter in globals():
                data[field.name] = globals()[getter](data, field)
                continue

            if field.name in generic_exclude_fields:
                continue

            if is_related:
                if is_related_many:
                    data[field.name] = []  # TODO: terminar
                else:
                    related_model = field.related_model.objects.all()
                    if related_model.exists():
                        data[field.name] = related_model[random.randint(0, len(related_model) - 1)]  # nosec
                    else:
                        # related_model is empty, continue.
                        continue

            elif choices:
                data[field.name] = choices[faker.pyint(min_value=0, max_value=len(choices) - 1)][0]
            else:
                if type == "BooleanField":
                    data[field.name] = faker.pybool()
                if type == "DecimalField":
                    data[field.name] = faker.pyfloat(
                        left_digits=random.randint(1, 4),  # nosec
                        right_digits=2,
                        positive=True,
                    )
                if type == "IntegerField":
                    data[field.name] = faker.pyint()
                if type == "CharField":
                    data[field.name] = faker.name()
                    data[field.name] = data[field.name][:max_size] if max_size else data[field.name]
                if type == "TextField":
                    data[field.name] = faker.text()
                    data[field.name] = data[field.name][:max_size] if max_size else data[field.name]
                if type == "EmailField":
                    data[field.name] = faker.email()
                    data[field.name] = data[field.name][:max_size] if max_size else data[field.name]
                if type == "DateTimeField":
                    data[field.name] = faker.date_time()
                if type == "DateField":
                    data[field.name] = faker.date()

                # Custom based on name
                if "image" in field.name:
                    data[field.name] = faker.image_url()

            if is_nullable and faker.boolean():
                data[field.name] = None

        if auto_add:
            data = model.objects.create(**data)
        return data
    except Exception as e:
        print(e)
        raise e


################################################################
# getters functions
# They are used to create test data based on a model and
# called with the format get_<model>_<field>
################################################################


def get_user_email(data, field):
    return data.get("username", faker.email())


def get_user_password(data, field):
    return global_password


def get_user_username(data, field):
    return data.get("email", faker.email())
