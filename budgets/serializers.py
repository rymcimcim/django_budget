from django.contrib.auth.models import User

from rest_framework import serializers

from budgets.models import BudgetCategories, MoneyFlow, MoneyFlowType
from utils import get_user_id_from_access_token


class OwnerPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        user_id = get_user_id_from_access_token(request)
        return User.objects.filter(pk=user_id)


class FamilyPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request')
        user_id = get_user_id_from_access_token(request)
        user = User.objects.get(pk=user_id)
        print(user.groups)
        return user.groups


class MoneyFlowSerializer(serializers.ModelSerializer):
    owner = OwnerPrimaryKeyRelatedField(many=False)
    family = FamilyPrimaryKeyRelatedField(many=False)
    shared = serializers.PrimaryKeyRelatedField(many=True, allow_null=True, queryset=User.objects.all())

    class Meta:
        model = MoneyFlow
        exclude = ('archived',)
    
    def validate(self, data):
        if data['money_flow_type'] == MoneyFlowType.INCOME.value and data['category'] != BudgetCategories.EX_INCOME.value:
            raise serializers.ValidationError('Income should have "External income" category.')
        
        if data['money_flow_type'] == MoneyFlowType.EXPENSE.value and data['category'] == BudgetCategories.EX_INCOME.value:
            raise serializers.ValidationError('Expense should have category different than "External income".')
        
        return data
