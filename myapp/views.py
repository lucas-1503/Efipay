from django.shortcuts import render, redirect
from django.views import View
from django.conf import settings
from .models import Charge, Boleto
from .forms import ChargeForm
from efipay import Endpoints
from django.http import JsonResponse
import json

endpoints = Endpoints(settings.CREDENTIALS)

class CreateChargeView(View):
    def get(self, request):
        form = ChargeForm()
        return render(request, 'create_charge.html', {'form': form})

    def post(self, request):
        form = ChargeForm(request.POST)
        if form.is_valid():
            charge = form.save(commit=False)
            
            charge.save()
            
            # Chamar a API da Efi para gerar o boleto
            body = {
    "items": [
        {
            "name": "Product 1",
            "value": int(charge.value * 100),  # Convertendo para centavos
            "amount": 1
        }
    ],
    "shippings": [
        {
            "name": "Default Shipping Cost",
            "value": 0
        }
    ],
    "payment": {
        "banking_billet": {
            "expire_at": "2024-12-31",
            "customer": {
                "name": charge.customer.user.get_full_name(),
                "email": charge.customer.user.email,
                "cpf": charge.customer.cpf,
                "birth": charge.customer.birth_date.strftime('%Y-%m-%d'),
                "phone_number": charge.customer.phone_number,
            },
            "configurations": {
                "fine": 1000,  # 10% de multa após o vencimento
                "interest": 33,  # 10% de juros após o vencimento
                "days_to_write_off": 30  # Excluir o boleto após 30 dias do vencimento
            }
        }
    }
}

            response = endpoints.create_one_step_charge(body=body)
            
            print(response)
            
            if response.get("error"):
                # Tratar erro
                return render(request, 'create_charge.html', {'form': form, 'error': response["error_description"]})
            
            boleto = Boleto.objects.create(
                charge=charge,
                expire_at=response["data"]["expire_at"],
                barcode=response["data"]["barcode"],
                pdf=response["data"]["pdf"]['charge'],
                status=response["data"]["status"],
                qrcode=response["data"]["pix"]["qrcode"],  # Salvar o QR code
                pix_key=response["data"]["pix"]["qrcode_image"]  # Salvar a chave Pix (ou a imagem do QR code, dependendo do que é retornado)
            )
            
            return redirect('charge_detail', charge_id=charge.id)

        return render(request, 'create_charge.html', {'form': form})

class ChargeDetailView(View):
    def get(self, request, charge_id):
        charge = Charge.objects.get(id=charge_id)
        return render(request, 'charge_detail.html', {'charge': charge})

def authenticate_view(request):
    status_code = endpoints.authenticate()
    if status_code == 200:
        token = endpoints.token  # O token está armazenado em endpoints.token
        print(token)
        return JsonResponse({"token": token})
    
    else:
        return JsonResponse({"error": "Authentication failed", "status_code": status_code})

