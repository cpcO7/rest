from django_filters import FilterSet, CharFilter


class CourseFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
