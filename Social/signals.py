from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import person, Receipt

@receiver(post_save, sender=person)
def create_or_update_receipt(sender, instance, **kwargs):

    if instance.payment_status == 'paid':
        receipt, created = Receipt.objects.get_or_create(shipment=instance)
        
        receipt.payment_status = 'paid'
        receipt.amount = instance.weight * 10 

        receipt.generate_pdf()
        
        receipt.save()
