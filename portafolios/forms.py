from django.forms import ModelForm
from .models import Portafolio

class PortafolioForm(ModelForm):
    class Meta:
        model = Portafolio
        fields = ["foto", "title", "description", "tags", "url", "private"]