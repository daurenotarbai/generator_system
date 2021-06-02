from django.shortcuts import render, redirect
from . import models
import csv, os
from faker import Faker
from datetime import datetime
from .forms import SchemaColumnsForm, SchemaBasicInfoForm

fake = Faker(['it_IT', 'en_US'])


def redirect_views(request):
    return redirect("/users/login")


def data_schemas_views(request):
    context = {}
    req_user = request.user
    query = models.TblSchemaBasicInfo.objects.filter(creator=req_user)
    context['request_user'] = req_user
    context['query'] = query
    return render(request, "generator_service/data_schemas.html", context=context)


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


def data_sets_views(request, id):
    context = {}
    req_user = request.user
    schema = models.TblSchemaBasicInfo.objects.get(id=id)
    query = models.TblDataSets.objects.filter(schema__id=id)
    context['request_user'] = req_user
    context['query'] = query
    context['schema'] = schema
    return render(request, "generator_service/data_sets.html", context=context)


def updating_schema_views(request, id):
    schema_name = request.POST.get("schema_name")
    column_separator = request.POST.get("column_separator")
    string_character = request.POST.get("string_character")

    name_column = request.POST.getlist("name_column")
    column_type = request.POST.getlist("column_type")
    int_from = request.POST.getlist("int_from")
    int_to = request.POST.getlist("int_to")
    sentences_number = request.POST.getlist("sentences_number")
    order = request.POST.getlist("order")

    schema = models.TblSchemaBasicInfo.objects.get(id=id)
    schema.schema_name = schema_name,
    schema.column_separator = column_separator,
    schema.string_character = string_character,
    schema.creator = request.user
    schema.save()

    for item in range(0, len(name_column)):
        columns = models.TblSchemaColumns.objects.filter(schema=schema)
        for column in columns:
            column.delete()

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
    columns = models.TblSchemaColumns.objects.filter(schema__id=schema_id)
    print("columns", columns)
    header = [column.column_name for column in columns]
    data = []
    for i in range(rows_number):
        row = []
        for column in columns:
            if column.column_type == "full_name":
                field = fake.name()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "address":
                field = fake.address()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "company":
                field = fake.company()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "job":
                field = fake.job()
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "email":
                field = fake.email()
                row.append(field)

            elif column.column_type == "phone":
                field = fake.phone_number()
                row.append(field)

            elif column.column_type == "text":
                field = fake.paragraph(nb_sentences=column.sentences_number)
                row.append(get_string(schema.string_character, field))

            elif column.column_type == "int":
                field = fake.random_int(min=column.int_from, max=column.int_to)
                row.append(field)

            elif column.column_type == "date":
                field = fake.date()
                row.append(field)
        data.append(row)

    folder_csv_file_path = 'media/' + str(datetime.now().strftime("%Y-%m-%d"))
    create_new_folder(folder_csv_file_path)

    number_of_datasets = models.TblDataSets.objects.filter(schema=schema).count()
    csv_file_path = folder_csv_file_path + '/' + schema.schema_name + str(number_of_datasets) + '.csv'

    with open(csv_file_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f,
                            delimiter=schema.column_separator,
                            lineterminator='\r\n',
                            quotechar=get_quotechar(schema.string_character))
        writer.writerow(header)
        writer.writerows(data)

        dataset_model = models.TblDataSets(schema=schema, status="process", csv_file=csv_file_path,
                                           rows_number=rows_number)
        dataset_model.save()
    return redirect('/data-sets/' + str(schema.id))


def get_quotechar(string_character):
    if string_character == '"' or string_character == '"""':
        return "'"

    if string_character == "'" or string_character == "'''":
        return '"'


def get_string(string_character, field):
    if string_character == "()" or string_character == '[]':
        string = string_character[-2] + field + string_character[-1]
    else:
        string = string_character + field + string_character
    return string
