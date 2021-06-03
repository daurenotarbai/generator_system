from django.shortcuts import render, redirect
from . import models
import os
from faker import Faker
from datetime import datetime
from .forms import SchemaColumnsForm, SchemaBasicInfoForm
from .tasks import write_to_csv
from django.contrib.auth.decorators import login_required
from django_celery_results.models import TaskResult

fake = Faker(['it_IT', 'en_US'])


def redirect_views(request):
    return redirect("/users/login")


@login_required(login_url='/users/login/')
def data_schemas_views(request):
    context = {}
    req_user = request.user
    query = models.TblSchemaBasicInfo.objects.filter(creator=req_user)
    context['request_user'] = req_user
    context['query'] = query
    return render(request, "generator_service/data_schemas.html", context=context)


@login_required(login_url='/users/login/')
def new_schema_views(request):
    context = {}
    form_column_schema = SchemaColumnsForm()
    form_basic_schema_info = SchemaBasicInfoForm()
    req_user = request.user
    query = models.TblSchemaBasicInfo.objects.filter(creator=req_user)
    context['request_user'] = req_user
    context['query'] = query
    context['form_column_schema'] = form_column_schema
    context['form_basic_schema_info'] = form_basic_schema_info
    return render(request, "generator_service/new_schema.html", context=context)


@login_required(login_url='/users/login/')
def edit_schema_views(request, id):
    context = {}
    form_column_schema = SchemaColumnsForm()
    form_basic_schema_info = SchemaBasicInfoForm()
    req_user = request.user
    columns = models.TblSchemaColumns.objects.filter(schema__id=id)
    query = models.TblSchemaBasicInfo.objects.get(id=id)
    context['request_user'] = req_user
    context['query'] = query
    context['columns'] = columns
    context['form_column_schema'] = form_column_schema
    context['form_basic_schema_info'] = form_basic_schema_info
    return render(request, "generator_service/edit_schema.html", context=context)

@login_required(login_url='/users/login/')
def delete_schema_views(request, id):
    query = models.TblSchemaBasicInfo.objects.get(id=id)
    query.delete()
    return redirect('/data-schemas')

@login_required(login_url='/users/login/')
def data_sets_views(request, id):
    context = {}
    req_user = request.user
    print(write_to_csv)
    schema = models.TblSchemaBasicInfo.objects.get(id=id)
    query = models.TblDataSets.objects.filter(schema__id=id)
    for item in query:
        try:
            task_status = TaskResult.objects.get(task_id=item.task_id).status
        except:
            task_status = "PENDING"
        item.task_status = task_status
        if item.task_status=="SUCCESS":
            item.status = "ready"
        else:
            item.status = "on process"
        item.save()


    context['request_user'] = req_user
    context['query'] = query
    context['schema'] = schema

    return render(request, "generator_service/data_sets.html", context=context)


def updating_schema_views(request, id):
    schema_name = request.POST.get("schema_name")
    print("schema_name",schema_name)
    column_separator = request.POST.get("column_separator")
    string_character = request.POST.get("string_character")

    name_column = request.POST.getlist("name_column")
    column_type = request.POST.getlist("column_type")
    int_from = request.POST.getlist("int_from")
    int_to = request.POST.getlist("int_to")
    sentences_number = request.POST.getlist("sentences_number")
    order = request.POST.getlist("order")

    schema = models.TblSchemaBasicInfo.objects.get(id=id)
    schema.schema_name = str(schema_name),
    schema.column_separator = column_separator,
    schema.string_character = string_character,
    schema.save()

    columns = models.TblSchemaColumns.objects.filter(schema=schema)
    for column in columns:
        column.delete()
    for item in range(0, len(name_column)):
        new_column = models.TblSchemaColumns.objects.create(
            schema=schema,
            column_name=name_column[item],
            column_type=column_type[item],
            int_from=int_from[item],
            int_to=int_to[item],
            sentences_number=sentences_number[item],
            order=order[item]
        )
        new_column.save()
    return redirect("/data-schemas")


def create_new_folder(local_dir):
    new_path = local_dir
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


def adding_new_schema_views(request):
    schema_name = request.POST.get("schema_name")
    column_separator = request.POST.get("column_separator")
    string_character = request.POST.get("string_character")

    name_column = request.POST.getlist("name_column")
    column_type = request.POST.getlist("column_type")
    int_from = request.POST.getlist("int_from")
    int_to = request.POST.getlist("int_to")
    sentences_number = request.POST.getlist("sentences_number")
    order = request.POST.getlist("order")

    new_schema = models.TblSchemaBasicInfo(
        schema_name=schema_name,
        column_separator=column_separator,
        string_character=string_character,
        creator=request.user)
    new_schema.save()

    for item in range(0, len(name_column)):
        new_column = models.TblSchemaColumns.objects.create(
            schema=new_schema,
            column_name=name_column[item],
            column_type=column_type[item],
            int_from=int_from[item],
            int_to=int_to[item],
            sentences_number=sentences_number[item],
            order=order[item]
        )
        new_column.save()
    return redirect("/data-schemas")


def generate_data_views(request, id):
    schema_id = id
    rows_number = int(request.GET.get("rows_number"))
    print("rows_number", rows_number)
    schema = models.TblSchemaBasicInfo.objects.get(id=schema_id)

    folder_csv_file_path = 'media/' + str(datetime.now().strftime("%Y-%m-%d"))
    create_new_folder(folder_csv_file_path)

    number_of_datasets = models.TblDataSets.objects.filter(schema=schema).count()
    csv_file_path = folder_csv_file_path + '/' + schema.schema_name + str(number_of_datasets) + '.csv'

    data = write_to_csv(csv_file_path,schema_id,rows_number)

    # print( write_to_csv.delay(csv_file_path,schema_id,rows_number))
    # print(data.task_id)

    dataset_model = models.TblDataSets(schema=schema, status="process", csv_file=csv_file_path,
                                       rows_number=rows_number,task_id="data.task_id")
    dataset_model.save()
    return redirect('/data-sets/' + str(schema.id))
