from django.shortcuts import render

# Create your views here.
from .forms import ExcelUploadForm
from django.http import HttpResponse
from .data_pipeline import extract_data_process,extract_single_col, clean_data_process,load_to_db
import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from .forms import ExcelUploadForm
from entities.models import Agent
from core.models import Commission
from django.contrib.admin.views.decorators import staff_member_required

pipeline_configuration = {
        "Agent ID": {
            "target_key": "agent_cid", 
            "type_cast": int, 
            "required": True
        },
        "Total commission to be paid": {
            "target_key": "total_commission_today", 
            # Safely casts to float and eliminates trailing float anomalies by rounding to 2 decimals
            "type_cast": lambda val: round(float(val), 2) if val is not None else 0.0, 
            "default": 0.0
        }
}

@staff_member_required
def commission_data_ingestion(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            excel_file = form.cleaned_data["excel_file"]

            # Process your ETL Data
            #print(excel_file.name)
            try:
                #print(extract_data_process(excel_file))
                

                # 1. Add message to Django framework (good for fallback logging)
                messages.success(request, "The ETL Data Load processed successfully.")
                payload = extract_data_process(excel_file, pipeline_configuration)
                print(payload)
                # objects = [
                #     Commission(
                #         agent=row["agent_id"],
                #         total_commission_today=row["total_commission_today"]
                #     )
                #     for row in payload
                # ]
                agent_map = {
                a.agent_cid: a
                for a in Agent.objects.filter(
                    agent_cid__in=[row["agent_cid"] for row in payload]
                )
                }
            
                objects = [
                    Commission.objects.update_or_create(
                        agent=agent_map[row["agent_cid"]],
                        defaults={
                            "total_commission_today": row["total_commission_today"]
                        }
                    )[0]
                    for row in payload
                ]
                #agent_values = extract_single_col(excel_file,col_name='Agent ID')
                #instances = [Agent(agent_id=value) for value in agent_values]
                ## AgentCommission.objects.bulk_create(objects)
                #Agent.objects.bulk_create(
                #instances,
                #update_conflicts=True,
                #unique_fields=["agent_id"],     # The field that must be unique
                #update_fields=["agent_id"],     # Fields to update if the name exists
                #)
                # 2. Return HTTP Response with HTMX Trigger Header to show SweetAlert
                response = HttpResponse("Success")
            except Exception as e:
                print(e)
                messages.error(request, f"Error occurred: {e}")
                return HttpResponse("Failed", status=500)
        else:
            # If form fails validation, re-render form with errors
            return render(
                request, "scribework/data-ingestion.html", {"form": form}
            )

    else:
        form = ExcelUploadForm()

    return render(
        request,
        "scribework/data-ingestion.html",
        {
            "form": form,
        },
    )