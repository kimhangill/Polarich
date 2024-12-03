from django.db import models

#예적금 리스트
class BaseProducts(models.Model):
    fin_prdt_cd=models.TextField(unique=True)
    kor_co_nm=models.TextField()
    fin_prdt_nm=models.TextField()
    etc_note=models.TextField()
    join_deny=models.IntegerField()
    join_member=models.TextField()
    join_way=models.TextField()
    spcl_cnd=models.TextField()

    class Meta:
        abstract = True

class DepositProducts(BaseProducts):
    pass
class SavingProducts(BaseProducts):
    pass

#예적금 옵션
class BaseOptions(models.Model):
    fin_prdt_cd=models.TextField()
    intr_rate_type_nm=models.CharField(max_length=100)
    intr_rate=models.FloatField(default=-10)
    intr_rate2=models.FloatField(default=-10)
    save_trm=models.IntegerField()
    class Meta:
        abstract = True

class DepositOptions(BaseOptions):
    product=models.ForeignKey("DepositProducts", on_delete=models.CASCADE, related_name='options')

class SavingOptions(BaseOptions):
    product=models.ForeignKey("SavingProducts", on_delete=models.CASCADE, related_name='options')


#개인신용대출 리스트
class creditLoanProducts(models.Model):
    fin_prdt_cd=models.TextField(unique=True)
    kor_co_nm=models.TextField()
    fin_prdt_nm=models.TextField()
    crdt_prdt_type=models.TextField()
    crdt_prdt_type_nm=models.TextField()
    join_way=models.TextField()

class creditLoanOptions(models.Model):
    product=models.ForeignKey("creditLoanProducts", on_delete=models.CASCADE, related_name='options')
    crdt_lend_rate_type=models.TextField()
    crdt_lend_rate_type_nm=models.TextField()
    crdt_grad_1=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_4=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_5=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_6=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_10=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_11=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_12=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_13=models.FloatField(default=-10, blank=True, null=True)
    crdt_grad_avg=models.FloatField(default=-10, blank=True, null=True)