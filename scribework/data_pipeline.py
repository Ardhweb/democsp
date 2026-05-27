# #ETL - process to load  upload file data into  respective tables into db with clean.
from openpyxl import Workbook, load_workbook
wb = Workbook()
ws = wb.active


# def extract_data_process(excel_file, **kwargs):
#     wb = load_workbook(excel_file)
#     ws = wb.active
#     #print(f"Active Sheet Title: {ws.title}")
#     #print("---")
    
#     agent_col = None
#     commission_col = None
#     # # Search first row
#     for cell in ws[1]:
#         if cell.value == "Agent ID":
#             agent_col = cell.column
#         elif cell.value == "Total commission to be paid": # Change this to your exact header name
#             commission_col = cell.column

#     agent_data = next(
#         ws.iter_cols(
#             min_col=agent_col,
#             max_col=agent_col,
#             min_row=2
#         )
#     )
    
#     commission_data = next(
#         ws.iter_cols(
#             min_col=commission_col,
#             max_col=commission_col,
#             min_row=2
#         )
#     )
    
#     for agent_cell, commission_cell in zip(agent_data, commission_data):
#         data[agent_cell.value] = commission_cell.value
    
#     print(data)
#     return data


def extract_single_col(excel_file,col_name):
    wb = load_workbook(excel_file)
    ws = wb.active
    col_name = None
    data = []
    # Seach first row
    for cell in ws[1]:
        if cell.value == "Agent ID":
            col_name = cell.column
    
    if col_name:
        col_data = next(ws.iter_cols(min_col=col_name, max_col=col_name, min_row=2))
        for cell in col_data:
            print(cell.value)
            data.append(cell.value)        
    else:
        print("Error: Could not find both 'Agent ID' and 'Total Commission' columns.")
    print(data)
    return data



# '''
# valuesonly
# for row in ws.values:
#    for value in row:
#      print(value)

# for row in ws.iter_rows(min_row=1, max_col=3, max_row=2, values_only=True):
#   print(row)

#  '''
# def clean_data_process():
#     pass

# def load_to_db():
#     pass


'''
ETL Process


 '''

 # ETL - process to load upload file data into respective tables into db with clean.
# from openpyxl import load_workbook
# from datetime import datetime

# # -------------------------------------------------------------------------
# # ETL PIPELINE CHANNELS (Fully Dynamic)
# # -------------------------------------------------------------------------

# def extract_data_process(excel_file, column_config):
#     wb = load_workbook(excel_file)
#     ws = wb.active

#     headers = {}
#     for cell in ws[1]:
#         if cell.value:
#             headers[cell.value] = cell.column

#     # Verify all configured excel headers exist in the sheet
#     for excel_header in column_config.keys():
#         if excel_header not in headers:
#             raise ValueError(f"Required column '{excel_header}' not found in the excel sheet.")

#     extracted_data = []

#     for row in ws.iter_rows(min_row=2, values_only=True):
#         row_data = {}
#         for excel_header, config in column_config.items():
#             col_idx = headers[excel_header] - 1
#             target_key = config["target_key"]
#             row_data[target_key] = row[col_idx] if col_idx < len(row) else None
#         extracted_data.append(row_data)

#     print(f"STEP 1 - EXTRACT COMPLETED ({len(extracted_data)} rows extracted)")
#     return clean_data_process(extracted_data, column_config)


# def clean_data_process(extracted_data, column_config):
#     cleaned_data = []

#     for row in extracted_data:
#         cleaned_row = {}
#         skip_row = False

#         for _, config in column_config.items():
#             target_key = config["target_key"]
#             type_cast = config.get("type_cast")
#             default_val = config.get("default")
#             is_required = config.get("required", False)
            
#             raw_value = row.get(target_key)

#             # Handle missing values
#             if raw_value is None or str(raw_value).strip() == "":
#                 if is_required:
#                     skip_row = True
#                     break
#                 else:
#                     cleaned_row[target_key] = default_val
#                     continue

#             # Handle dynamic formatting/casting
#             if type_cast:
#                 try:
#                     # Works for functions like int, float, str, or custom lambdas
#                     cleaned_row[target_key] = type_cast(raw_value)
#                 except (ValueError, TypeError):
#                     if is_required:
#                         skip_row = True
#                         break
#                     else:
#                         cleaned_row[target_key] = default_val
#             else:
#                 cleaned_row[target_key] = raw_value

#         if not skip_row:
#             cleaned_data.append(cleaned_row)

#     print(f"STEP 2 - CLEAN COMPLETED ({len(cleaned_data)} rows valid)")
#     return load_to_db(cleaned_data, column_config)


# def load_to_db(cleaned_data, column_config):
#     orm_payload = []

#     for row in cleaned_data:
#         payload_item = {}
#         for _, config in column_config.items():
#             target_key = config["target_key"]
#             payload_item[target_key] = row[target_key]
#         orm_payload.append(payload_item)

#     print("STEP 3 - LOAD PAYLOAD READY")
#     return orm_payload


import os
from datetime import datetime
from openpyxl import load_workbook

# -------------------------------------------------------------------------
# 1. CELERY CONFIGURATION & TASK WRAPPER (Future Use)
# -------------------------------------------------------------------------
# To switch to background execution later:
# 1. Install celery: pip install celery redis
# 2. Uncomment the Celery initialization and decorator code below.

# from celery import Celery
# app = Celery('excel_tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# @app.task(name="tasks.run_dynamic_pipeline")
def run_pipeline_task(excel_file, column_config):
    """
    Celery-ready worker entry point.
    Call with: run_pipeline_task.delay("path/to/file.xlsx", config)
    """
    print(f"[Celery Worker] Processing file: {excel_file}")
    return extract_data_process(excel_file, column_config)


# -------------------------------------------------------------------------
# 2. THE DYNAMIC ETL PIPELINE ENGINE
# -------------------------------------------------------------------------

def extract_data_process(excel_file, column_config):
    """
    STEP 1: Extract data dynamically based on configuration headers.
    """
    wb = load_workbook(excel_file)
    ws = wb.active

    headers = {}
    # Maps header text to column indexes dynamically
    for cell in ws[1]:
        if cell.value:
            headers[cell.value] = cell.column

    # Verify that all configured excel headers actually exist in the file
    for excel_header in column_config.keys():
        if excel_header not in headers:
            raise ValueError(f"Required column '{excel_header}' not found in Excel sheet.")

    extracted_data = []

    # Iterates row wise, tracking data via target keys
    for row in ws.iter_rows(min_row=2, values_only=True):
        row_data = {}
        for excel_header, config in column_config.items():
            col_idx = headers[excel_header] - 1
            target_key = config["target_key"]
            row_data[target_key] = row[col_idx] if col_idx < len(row) else None
        extracted_data.append(row_data)

    print(f"--- STEP 1 - EXTRACT COMPLETED ({len(extracted_data)} rows read) ---")
    return clean_data_process(extracted_data, column_config)


def clean_data_process(extracted_data, column_config):
    """
    STEP 2: Clean, type-cast, format, and filter data dynamically.
    """
    cleaned_data = []

    for row in extracted_data:
        cleaned_row = {}
        skip_row = False

        for _, config in column_config.items():
            target_key = config["target_key"]
            type_cast = config.get("type_cast")
            default_val = config.get("default")
            is_required = config.get("required", False)
            
            raw_value = row.get(target_key)

            # Check for empty or blank values
            if raw_value is None or str(raw_value).strip() == "":
                if is_required:
                    skip_row = True
                    break
                else:
                    cleaned_row[target_key] = default_val
                    continue

            # Run transformation rules / functions
            if type_cast:
                try:
                    cleaned_row[target_key] = type_cast(raw_value)
                except (ValueError, TypeError):
                    if is_required:
                        skip_row = True  # Block broken/corrupt critical rows
                        break
                    else:
                        cleaned_row[target_key] = default_val
            else:
                cleaned_row[target_key] = raw_value

        if not skip_row:
            cleaned_data.append(cleaned_row)

    print(f"--- STEP 2 - CLEAN COMPLETED ({len(cleaned_data)} rows validated) ---")
    return load_to_db(cleaned_data, column_config)


def load_to_db(cleaned_data, column_config):
    """
    STEP 3: Format into a pure database ready ORM payload.
    """
    orm_payload = []

    for row in cleaned_data:
        payload_item = {}
        for _, config in column_config.items():
            target_key = config["target_key"]
            payload_item[target_key] = row[target_key]
        orm_payload.append(payload_item)

    print("--- STEP 3 - LOAD PAYLOAD READY ---")
    return orm_payload


# -------------------------------------------------------------------------
# 3. RUNTIME / HOW TO CALL EXAMPLES
# -------------------------------------------------------------------------
'''
if __name__ == "__main__":
    
    # Define rules here. Easily expandable to 3, 5, or 20+ columns.
    pipeline_configuration = {
        "Agent ID": {
            "target_key": "agent_id", 
            "type_cast": int, 
            "required": True
        },
        "Total commission to be paid": {
            "target_key": "commission", 
            # Safely casts to float and eliminates trailing float anomalies by rounding to 2 decimals
            "type_cast": lambda val: round(float(val), 2) if val is not None else 0.0, 
            "default": 0.0
        }
    }

'''