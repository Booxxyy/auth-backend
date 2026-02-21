from django.core.management.base import BaseCommand
from access_control.models import Role, BusinessElement, AccessRoleRule


class Command(BaseCommand):
    help = 'Заполняет БД тестовыми данными'

    def handle(self, *args, **kwargs):
        # Роли
        admin, _ = Role.objects.get_or_create(name='admin', defaults={'description': 'Администратор'})
        manager, _ = Role.objects.get_or_create(name='manager', defaults={'description': 'Менеджер'})
        user, _ = Role.objects.get_or_create(name='user', defaults={'description': 'Пользователь'})
        guest, _ = Role.objects.get_or_create(name='guest', defaults={'description': 'Гость'})

        # Объекты
        users_el, _ = BusinessElement.objects.get_or_create(name='users', defaults={'description': 'Пользователи'})
        products_el, _ = BusinessElement.objects.get_or_create(name='products', defaults={'description': 'Товары'})
        orders_el, _ = BusinessElement.objects.get_or_create(name='orders', defaults={'description': 'Заказы'})
        rules_el, _ = BusinessElement.objects.get_or_create(name='access_rules', defaults={'description': 'Правила доступа'})

        # Правила — admin (всё разрешено)
        AccessRoleRule.objects.get_or_create(role=admin, element=users_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=True,
            update_permission=True, update_all_permission=True, delete_permission=True, delete_all_permission=True
        ))
        AccessRoleRule.objects.get_or_create(role=admin, element=products_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=True,
            update_permission=True, update_all_permission=True, delete_permission=True, delete_all_permission=True
        ))
        AccessRoleRule.objects.get_or_create(role=admin, element=orders_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=True,
            update_permission=True, update_all_permission=True, delete_permission=True, delete_all_permission=True
        ))
        AccessRoleRule.objects.get_or_create(role=admin, element=rules_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=True,
            update_permission=True, update_all_permission=True, delete_permission=True, delete_all_permission=True
        ))

        # Правила — manager
        AccessRoleRule.objects.get_or_create(role=manager, element=products_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=True,
            update_permission=True, update_all_permission=True, delete_permission=False, delete_all_permission=False
        ))
        AccessRoleRule.objects.get_or_create(role=manager, element=orders_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=True,
            update_permission=True, update_all_permission=True, delete_permission=False, delete_all_permission=False
        ))

        # Правила — user
        AccessRoleRule.objects.get_or_create(role=user, element=products_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=False,
            update_permission=False, update_all_permission=False, delete_permission=False, delete_all_permission=False
        ))
        AccessRoleRule.objects.get_or_create(role=user, element=orders_el, defaults=dict(
            read_permission=True, read_all_permission=False, create_permission=True,
            update_permission=True, update_all_permission=False, delete_permission=True, delete_all_permission=False
        ))

        # Правила — guest
        AccessRoleRule.objects.get_or_create(role=guest, element=products_el, defaults=dict(
            read_permission=True, read_all_permission=True, create_permission=False,
            update_permission=False, update_all_permission=False, delete_permission=False, delete_all_permission=False
        ))

        self.stdout.write(self.style.SUCCESS('✅ Тестовые данные успешно загружены!'))
