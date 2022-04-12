# Generated by Django 4.0.3 on 2022-04-12 09:22

from django.db import migrations

from ..models import Employee as EmployeeModel


def create_groups(apps, schema_migration):
    Employee = apps.get_model("employees", "Employee")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    add_employee = Permission.objects.get(codename="add_employee")
    change_employee = Permission.objects.get(codename="change_employee")
    delete_employee = Permission.objects.get(codename="delete_employee")
    view_employee = Permission.objects.get(codename="view_employee")

    add_client = Permission.objects.get(codename="add_client")
    change_client = Permission.objects.get(codename="change_client")
    delete_client = Permission.objects.get(codename="delete_client")
    view_client = Permission.objects.get(codename="view_client")

    add_company = Permission.objects.get(codename="add_company")
    change_company = Permission.objects.get(codename="change_company")
    delete_company = Permission.objects.get(codename="delete_company")
    view_company = Permission.objects.get(codename="view_company")

    add_contract = Permission.objects.get(codename="add_contract")
    change_contract = Permission.objects.get(codename="change_contract")
    delete_contract = Permission.objects.get(codename="delete_contract")
    view_contract = Permission.objects.get(codename="view_contract")

    add_event = Permission.objects.get(codename="add_event")
    change_event = Permission.objects.get(codename="change_event")
    delete_event = Permission.objects.get(codename="delete_event")
    view_event = Permission.objects.get(codename="view_event")

    # Sales.
    salesperson_permissions = [
        view_employee,
        view_client,
        add_client,
        view_company,
        add_company,
        view_event,
        add_event,
        view_contract,
        add_contract,
    ]

    sales_team = Group(name="sales")
    sales_team.save()

    sales_team.permissions.set(salesperson_permissions)

    # Support.
    support_consultant_permissions = [
        view_employee,
        view_client,
        view_company,
        view_contract,
        view_event,
    ]

    support_team = Group(name="support")
    support_team.save()

    support_team.permissions.set(support_consultant_permissions)

    # Management.
    manager_permissions = [
        view_employee,
        add_employee,
        change_employee,
        delete_employee,
        view_client,
        add_client,
        change_client,
        delete_client,
        view_company,
        add_company,
        change_company,
        delete_company,
        view_contract,
        add_contract,
        change_contract,
        delete_contract,
        view_event,
        add_event,
        change_event,
        delete_event,
    ]

    management_team = Group(name="management")
    management_team.save()

    management_team.permissions.set(manager_permissions)

    for employee in Employee.objects.all():
        if employee.role == EmployeeModel.SALES_PERSON:
            sales_team.user_set.add(employee)
        elif employee.role == EmployeeModel.SUPPORT_CONSULTANT:
            support_team.user_set.add(employee)
        elif employee.role == EmployeeModel.MANAGER:
            management_team.user_set.add(employee)


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0002_alter_employee_is_staff"),
    ]

    operations = [migrations.RunPython(create_groups)]