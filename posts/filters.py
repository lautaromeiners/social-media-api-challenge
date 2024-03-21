from django_filters import rest_framework as filters
from .models import Post


class PostFilter(filters.FilterSet):
    author_id = filters.NumberFilter(field_name="author__id", lookup_expr="exact")
    from_date = filters.DateFilter(field_name="created_at", lookup_expr="gte")
    to_date = filters.DateFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Post
        fields = ("author_id", "from_date", "to_date")
