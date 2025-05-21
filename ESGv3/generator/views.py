from django.shortcuts import render, redirect
from .generator import generate_columns

column_definitions = []
generation_parameters = {}

def index(request):
    global column_definitions

    if request.method == "POST":
        if "add_column" in request.POST:
            column_name = request.POST.getlist("column_name")
            column_prompt = request.POST.getlist("column_prompt")
            for column_name, column_prompt in zip(column_name, column_prompt):
                if column_name and column_prompt:
                    column_definitions.append((column_name, column_prompt))
            return redirect('generate')

    return render(request, "index.html")

def generate(request):
    global generation_parameters

    if request.method == "POST":
        if "generate_columns" in request.POST:
            generation_parameters = {
                'num_rows': int(request.POST.get("num_rows")),
                'file_name': request.POST.get("file_name"),
                'file_type': request.POST.get("file_type")
            }
            return redirect('end')

    return render(request, "generate.html")

def end(request):
    global column_definitions, generation_parameters

    if request.method == "POST":
        if "download_sheet" in request.POST:
            return generate_columns(column_definitions, generation_parameters['num_rows'], generation_parameters['file_name'], generation_parameters['file_type'])

    return render(request, "end.html")