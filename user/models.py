import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='纬度')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='经度')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址描述')
    
    class Meta:
        verbose_name = '位置'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.latitude}, {self.longitude} ({self.address or '无描述'})"

class VerificationCode(models.Model):
    phone = models.CharField(max_length=20, verbose_name='手机号')
    code = models.CharField(max_length=6, verbose_name='验证码')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    is_used = models.BooleanField(default=False, verbose_name='是否已使用')
    
    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return f"{self.phone} - {self.code}"


class Family(models.Model):
    family_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, verbose_name='家族ID')
    family_code = models.CharField(max_length=10, unique=True, verbose_name='家族编码')
    name = models.CharField(max_length=100, verbose_name='家族名称')
    description = models.TextField(blank=True, null=True, verbose_name='家族描述')
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name='families', verbose_name='家族位置')
    
    class Meta:
        verbose_name = '家族'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name
    
class Relationship(models.Model):
    relationship_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, verbose_name='关系ID')
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='from_user', verbose_name='关系发起人')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='to_user', verbose_name='关系接收人')
    relationship_type = models.CharField(max_length=50, choices=(('parent', '父母'), ('child', '子女'), ('sibling', '兄弟姐妹'), ('spouse', '配偶')), verbose_name='关系类型')
    status = models.CharField(max_length=20, choices=(('pending', '待处理'), ('accepted', '已接受'), ('rejected', '已拒绝')), default='pending', verbose_name='关系状态')
    details = models.TextField(blank=True, null=True, verbose_name='关系详情')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

class User(AbstractUser):
    # Override AbstractUser fields with verbose_name
    username = models.CharField(max_length=150, unique=True, verbose_name='用户名')
    first_name = models.CharField(max_length=150, blank=True, verbose_name='名')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='姓')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    is_staff = models.BooleanField(default=False, verbose_name='工作人员状态')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    
    # Custom fields
    birth_date = models.DateField(null=True, blank=True, verbose_name='生日')
    death_date = models.DateField(null=True, blank=True, verbose_name='死期')
    milk_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='乳名')
    birth_place = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name='birth_users', verbose_name='出生地')
    burial_place = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL, related_name='burial_users', verbose_name='墓地')
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True, verbose_name='手机号')
    phone_password = models.CharField(max_length=128, blank=True, null=True, verbose_name='手机号密码')
    family = models.ForeignKey(Family, null=True, blank=True, on_delete=models.SET_NULL, related_name='users', verbose_name='家族')
    gender = models.CharField(max_length=10, choices=(('male', '男'), ('female', '女'), ('other', '其他')), default='other', verbose_name='性别')

    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.username
