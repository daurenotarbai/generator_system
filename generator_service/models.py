from django.db import models
from django.contrib.auth.models import User

SEPARATOR_CHOICES = (
    (",", "Comma(,)"),
    ("|", "Forward slash (|)"),
    (";", "Semicolon(;)"),
)

STRING_CHARACTER_CHOICES = (
    ('"', 'Double-quote(")'),
    ("'", "Single-quote(')"),
    ("'''", "Triple-quote(''')"),
    ('"""', 'Triple-quote(""")'),
    ('()', 'Bracket(())'),
    ('[]', 'Straight Brackets([])'),
)


class TblSchemaBasicInfo(models.Model):
    schema_name = models.CharField(max_length=20, null=True)
    column_separator = models.CharField(max_length=15, choices=SEPARATOR_CHOICES, default=";")
    string_character = models.CharField(max_length=15, choices=STRING_CHARACTER_CHOICES, default="'")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updated_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = "mdl_schema_basic_info"
        verbose_name = 'Структура файла'
        verbose_name_plural = 'Структура файлы'

    def __str__(self):
        return str(self.id)


TYPE_CHOICES = (
    ("full_name", "Full Name"),
    ("company", "Company"),
    ("address", "Address"),
    ("job", "Job"),
    ("email", "Email"),
    ("phone", "Phone"),
    ("text", "Text"),
    ("int", "Integer"),
    ("date", "Date"),
)


class TblSchemaColumns(models.Model):
    column_name = models.CharField(max_length=20, default='', null=True)
    column_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default="full_name")
    schema = models.ForeignKey(TblSchemaBasicInfo, on_delete=models.CASCADE, null=True)
    int_from = models.PositiveIntegerField(default=0, null=True)
    int_to = models.PositiveIntegerField(default=0, null=True)
    sentences_number = models.PositiveIntegerField(default=0, null=True)
    order = models.PositiveIntegerField(default=0, null=False)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = "mdl_schema_columns"
        verbose_name = 'Структура столбцы'
        verbose_name_plural = 'Структура столбцы'

    def __str__(self):
        return str(self.column_name)


STATUS_CHOICES = (
    ("ready", "ready"),
    ("process", "processing")
)


class TblDataSets(models.Model):
    schema = models.ForeignKey(TblSchemaBasicInfo, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default="process")
    csv_file = models.CharField(max_length=300, default='', null=True)
    rows_number = models.PositiveIntegerField(default=0, null=True)
    task_id = models.CharField(max_length=300, default='', null=True)
    task_status = models.CharField(max_length=40, default='', null=True)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        db_table = "mdl_datasets"
        verbose_name = 'Набор данных'
        verbose_name_plural = 'Наборы данных'

    def __str__(self):
        return str(self.schema)
