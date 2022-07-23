from celery import shared_task
from django.db.models import Q

from .models import User, UserMove, Company


@shared_task
def lar_widget(company_id, lon, lot):
    company = User.objects.filter(Q(company_id=company_id) & (Q(role="manager") | Q(role="agent")))

# user = User.objects.get(id=user_id)

# w.lon = lon
# w.lot = lot
# w.save()
