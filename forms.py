from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, DecimalField, IntegerField, BooleanField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
from flask_wtf.file import FileAllowed

# Authentication Forms
class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Senha Atual', validators=[DataRequired()])
    new_password = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Alterar Senha')

# Employee Forms
class EmployeeForm(FlaskForm):
    first_name = StringField('Nome', validators=[DataRequired()])
    last_name = StringField('Sobrenome', validators=[DataRequired()])
    position = StringField('Cargo', validators=[DataRequired()])
    department = StringField('Departamento', validators=[DataRequired()])
    phone = StringField('Telefone', validators=[DataRequired()])
    hire_date = DateField('Data de Contratação', format='%Y-%m-%d', validators=[DataRequired()])
    active = BooleanField('Ativo')
    
    # User account details
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Nível de Acesso', choices=[
        ('employee', 'Funcionário'), 
        ('management', 'Gerência'), 
        ('admin', 'Administrador')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Salvar')

class EditEmployeeForm(FlaskForm):
    first_name = StringField('Nome', validators=[DataRequired()])
    last_name = StringField('Sobrenome', validators=[DataRequired()])
    position = StringField('Cargo', validators=[DataRequired()])
    department = StringField('Departamento', validators=[DataRequired()])
    phone = StringField('Telefone', validators=[DataRequired()])
    hire_date = DateField('Data de Contratação', format='%Y-%m-%d', validators=[DataRequired()])
    active = BooleanField('Ativo')
    
    # User account details - password is optional for edit
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Nível de Acesso', choices=[
        ('employee', 'Funcionário'), 
        ('management', 'Gerência'), 
        ('admin', 'Administrador')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Atualizar')

# Client/Supplier Forms
class ClientForm(FlaskForm):
    name = StringField('Nome/Empresa', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefone', validators=[DataRequired()])
    address = StringField('Endereço', validators=[DataRequired()])
    city = StringField('Cidade', validators=[DataRequired()])
    state = StringField('Estado', validators=[DataRequired()])
    zip_code = StringField('CEP', validators=[DataRequired()])
    contact_person = StringField('Pessoa de Contato', validators=[Optional()])
    active = BooleanField('Ativo', default=True)
    
    submit = SubmitField('Salvar')

class SupplierForm(FlaskForm):
    name = StringField('Nome/Empresa', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Telefone', validators=[DataRequired()])
    address = StringField('Endereço', validators=[DataRequired()])
    city = StringField('Cidade', validators=[DataRequired()])
    state = StringField('Estado', validators=[DataRequired()])
    zip_code = StringField('CEP', validators=[DataRequired()])
    contact_person = StringField('Pessoa de Contato', validators=[Optional()])
    active = BooleanField('Ativo', default=True)
    
    submit = SubmitField('Salvar')

# Service Order Forms
class ServiceOrderForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('open', 'Aberta'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada')
    ], validators=[DataRequired()])
    priority = SelectField('Prioridade', choices=[
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta')
    ], validators=[DataRequired()])
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    employee_id = SelectField('Responsável', coerce=int, validators=[DataRequired()])
    start_date = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired()])
    completion_date = DateField('Data de Conclusão', format='%Y-%m-%d', validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional()])
    
    submit = SubmitField('Salvar')

# Project Forms
class ProjectForm(FlaskForm):
    name = StringField('Nome do Projeto', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('planning', 'Planejamento'),
        ('in_progress', 'Em Andamento'),
        ('on_hold', 'Em Espera'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado')
    ], validators=[DataRequired()])
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    manager_id = SelectField('Gerente do Projeto', coerce=int, validators=[DataRequired()])
    start_date = DateField('Data de Início', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Data de Conclusão Prevista', format='%Y-%m-%d', validators=[Optional()])
    budget = DecimalField('Orçamento', validators=[Optional(), NumberRange(min=0)])
    
    submit = SubmitField('Salvar')

# Inventory Forms
class InventoryItemForm(FlaskForm):
    name = StringField('Nome do Item', validators=[DataRequired()])
    description = TextAreaField('Descrição', validators=[Optional()])
    sku = StringField('SKU/Código', validators=[DataRequired()])
    category = StringField('Categoria', validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    minimum_stock = IntegerField('Estoque Mínimo', validators=[DataRequired(), NumberRange(min=0)])
    unit_price = DecimalField('Preço Unitário', validators=[DataRequired(), NumberRange(min=0)])
    location = StringField('Localização', validators=[Optional()])
    supplier_id = SelectField('Fornecedor', coerce=int, validators=[Optional()])
    
    submit = SubmitField('Salvar')

# Finance Forms
class FinancialEntryForm(FlaskForm):
    type = SelectField('Tipo', choices=[
        ('income', 'Receita'),
        ('expense', 'Despesa')
    ], validators=[DataRequired()])
    category = StringField('Categoria', validators=[DataRequired()])
    amount = DecimalField('Valor', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    date = DateField('Data', format='%Y-%m-%d', validators=[DataRequired()])
    invoice_number = StringField('Número da Fatura/Nota Fiscal', validators=[Optional()])
    payment_method = SelectField('Método de Pagamento', choices=[
        ('money', 'Dinheiro'),
        ('credit_card', 'Cartão de Crédito'),
        ('debit_card', 'Cartão de Débito'),
        ('bank_transfer', 'Transferência Bancária'),
        ('check', 'Cheque'),
        ('other', 'Outro')
    ], validators=[DataRequired()])
    client_id = SelectField('Cliente', coerce=int, validators=[Optional()])
    supplier_id = SelectField('Fornecedor', coerce=int, validators=[Optional()])
    service_order_id = SelectField('Ordem de Serviço', coerce=int, validators=[Optional()])
    project_id = SelectField('Projeto', coerce=int, validators=[Optional()])
    invoice_file = FileField('Anexar Documento', validators=[
        Optional(),
        FileAllowed(['pdf', 'jpg', 'png'], 'Somente arquivos PDF, JPG ou PNG são permitidos.')
    ])
    
    submit = SubmitField('Salvar')

# Order Item Forms
class OrderItemForm(FlaskForm):
    inventory_item_id = SelectField('Item', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1)])
    service_order_id = HiddenField('Ordem de Serviço ID')
    
    submit = SubmitField('Adicionar Item')

# Search Forms
class SearchForm(FlaskForm):
    query = StringField('Buscar', validators=[Optional()])
    status = SelectField('Status', validators=[Optional()], choices=[
        ('', 'Todos'),
        ('open', 'Aberta'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluída'),
        ('cancelled', 'Cancelada')
    ])
    date_from = DateField('De', format='%Y-%m-%d', validators=[Optional()])
    date_to = DateField('Até', format='%Y-%m-%d', validators=[Optional()])
    
    submit = SubmitField('Buscar')
