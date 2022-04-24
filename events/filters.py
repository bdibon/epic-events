import django_filters


class EventFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(
        field_name="client__last_name", lookup_expr="iexact"
    )
    client_email = django_filters.CharFilter(
        field_name="client__email", lookup_expr="iexact"
    )
    date = django_filters.DateFilter()


class ContractFilter(django_filters.FilterSet):
    client_name = django_filters.CharFilter(
        field_name="client__last_name", lookup_expr="iexact"
    )
    client_email = django_filters.CharFilter(
        field_name="client__email", lookup_expr="iexact"
    )
    date = django_filters.DateFilter(field_name="created_at")
    amount = django_filters.NumberFilter()
