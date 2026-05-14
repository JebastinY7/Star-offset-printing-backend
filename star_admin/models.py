from django.db import models
from django.contrib.auth.models import User
from pricing.models import Category, Size, Variant

# Create your models here.
    
# Customers
class Customer(models.Model):
    Customer_code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=50)
    is_member = models.BooleanField(default=False)
    member_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points = models.IntegerField(default=0)
    join_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Bills Table
class Bill(models.Model):
    bill_no = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gross_total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    points_used = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    current_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    old_due_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    previous_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra_charge_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(
        max_length=20,
        choices=[('paid', 'Paid'), ('partial', 'Partial'), ('due', 'Due')],
        default='paid'
    )
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.bill_no
    

# Bill Items Table
class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    extra_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra_purpose = models.CharField(max_length=255, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)


# Points Transaction
class PointTransaction(models.Model):
    TYPE_CHOICES = (
        ('earn', 'Earn'),
        ('redeem', 'Redeem'),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True)
    points_added = models.IntegerField(default=0)
    points_used = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)


# Settings Table
class Setting(models.Model):
    points_per_rupee = models.IntegerField(null=True, blank=True)
    max_redeem_percent = models.IntegerField(null=True, blank=True)
    membership_validity_days = models.IntegerField()
    renewal_fee = models.DecimalField(max_digits=10, decimal_places=2)
    shop_renewal_fee = models.DecimalField(max_digits=10, decimal_places=2)


# Offers
class OffersHistory(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    group = models.CharField(max_length=20)
    category = models.CharField(max_length=50)
    total_sent = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
#Membership Renewal
class MembershipTransaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('cash', 'Cash'),
            ('upi', 'UPI'),
            ('card', 'Card')
        ],
        default='cash'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

# Password Reset
class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)

# models.py
class LoginAttempt(models.Model):
    email = models.CharField(max_length=255)
    attempts = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

# Orders 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    work_name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)

    order_date = models.DateField()
    delivery_date = models.DateField()

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_billed = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('progress', 'In Progress'),
            ('completed', 'Completed'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled')
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.work_name}"
    
# OrderItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

# Staff Activity
class StaffActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(null=True, blank=True)