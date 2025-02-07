from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from io import BytesIO
from django.core.files.base import ContentFile

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.user.username} profile"

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} post"

class person(models.Model):
    order_id = models.CharField(max_length=16, unique=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, default='Unknown')
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    current_address = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    pickup_date = models.DateField()

    PAYMENT_METHOD_CHOICES = [
        ('credit-card', 'Credit Card'),
        ('debit-card', 'Debit Card'),
        ('upi', 'UPI'),
        ('other', 'Other'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='credit-card')
    payment_details = models.TextField(null=True, blank=True)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('transit', 'Transit'),
        ('processing', 'Processing'),
        ('cleared', 'Cleared'),
        ('detained', 'Detained'),
        ('despatched', 'Despatched')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded')
    ]
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    current_location = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def count_total_shipments(cls, user):
        return cls.objects.filter(user=user).count() if user else 0

class AgentProfile(models.Model):
    agent_id = models.CharField(max_length=16, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    password = models.CharField(max_length=50, default='Default')

    def __str__(self):
        return f"Agent {self.name} - ID: {self.agent_id}"

class Receipt(models.Model):
    shipment = models.OneToOneField(person, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=20, unique=True, blank=True)
    date_issued = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_status = models.CharField(max_length=10, choices=person.PAYMENT_STATUS_CHOICES, default='unpaid')
    pdf_file = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"Receipt {self.receipt_number} for Order ID {self.shipment.order_id}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"REC-{self.shipment.order_id}-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        super().save(*args, **kwargs)

    # def generate_pdf(self):
    #     buffer = BytesIO()
    #     p = canvas.Canvas(buffer)

    #     p.drawString(100, 750, f"Receipt Number: {self.receipt_number}")
    #     p.drawString(100, 730, f"Order ID: {self.shipment.order_id}")
    #     p.drawString(100, 710, f"Customer Name: {self.shipment.name}")
    #     p.drawString(100, 690, f"Amount: {self.amount}")
    #     p.drawString(100, 670, f"Payment Status: {self.payment_status}")
    #     p.drawString(100, 650, f"Issued Date: {self.date_issued.strftime('%Y-%m-%d')}")

    #     p.showPage()
    #     p.save()

    #     buffer.seek(0)
    #     self.pdf_file.save(f"receipt_{self.receipt_number}.pdf", ContentFile(buffer.read()), save=False)
    #     buffer.close()

@receiver(post_save, sender=person)
def create_or_update_receipt(sender, instance, created, **kwargs):
    if instance.payment_status == 'paid':
        receipt, _ = Receipt.objects.get_or_create(shipment=instance)
        receipt.payment_status = 'paid'
        receipt.amount = instance.weight * 10  # Example calculation
        receipt.generate_pdf()
        receipt.save()
