from django.contrib.auth.models import User, Group
from django.db import models
from typing_extensions import Self


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> Self:
        del using

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using='primary',
            update_fields=update_fields)
        
        super().save(
            force_insert=True,
            force_update=force_update,
            using='replica',
            update_fields=update_fields)

        return self.refresh_from_db(fields=('id',))
    
    def delete(self, using=None, keep_parents=False) -> Self:
        del using

        self.archived = True
        self.save()
        return self

    class Meta:
        abstract = True

# source: https://localfirstbank.com/article/budgeting-101-personal-budget-categories/
class BudgetCategories(models.TextChoices):
    HOUSING = 'Housing'
    TRANSPORTATION = 'Transportation'
    FOOD = 'Food'
    UTILITIES = 'Utilites'
    CLOTHING = 'Clothing'
    HEALTHCARE = 'Healthcare'
    INSURANCE = 'Insurance'
    SUPPLIES = 'Supplies'
    PERSONAL = 'Personal'
    DEBT = 'Debt'
    RETIREMENT = 'Retirement'
    EDUCATION = 'Education'
    SAVINGS = 'Savings'
    DONATIONS = 'Donations'
    ENTERTAINMENT = 'Entertainment'
    OTHER = 'Other'
    EX_INCOME = 'External income'


class MoneyFlowType(models.TextChoices):
    INCOME = 'income'
    EXPENSE = 'expense'


class MoneyFlow(BaseModel):
    money_flow_type = models.CharField(max_length=7, choices=MoneyFlowType.choices, db_index=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    short_desc = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, db_index=True)
    family = models.ForeignKey(Group, on_delete=models.PROTECT, db_index=True)
    archived = models.BooleanField(default=False, db_index=True)
    shared = models.ManyToManyField(User, blank=True, db_index=True, related_name='shared_money_flow')
    category = models.CharField(max_length=15, choices=BudgetCategories.choices, db_index=True)

    def __repr__(self) -> str:
        return f'{self.money_flow_type} {self.amount}-{self.owner_id}'
