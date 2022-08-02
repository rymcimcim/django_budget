from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from budgets.models import MoneyFlow, MoneyFlowType
from budgets.permissions import IsOwnerOrInSharedReadOnly
from budgets.serializers import MoneyFlowSerializer

from django_budget.db_routers import PrimaryReplicaRouter

from utils import get_user_id_from_access_token


def get_database_name():
    return PrimaryReplicaRouter().db_alias


class AdminMoneyFlowViewSet(viewsets.ModelViewSet):
    queryset = MoneyFlow.objects.using(get_database_name()).all()
    permission_classes = (IsAdminUser,)
    serializer_class = MoneyFlowSerializer


class MoneyFlowViewSet(viewsets.ModelViewSet):
    serializer_class = MoneyFlowSerializer
    permission_classes = (IsOwnerOrInSharedReadOnly,)

    def get_queryset(self):
        user_id = get_user_id_from_access_token(self.request)
        request_user = User.objects.get(pk=user_id)
        return MoneyFlow.objects.using(get_database_name())\
            .filter(
                (
                    Q(owner=request_user) |\
                    Q(family__in=request_user.groups.all()) |\
                    Q(shared__in=[request_user])
                ) & Q(archived=False)
            )
