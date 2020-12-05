from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional
from wtforms import ValidationError

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass 

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    login = StringField('Login', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
               'Os nomes de usuário devem ter apenas letras, números, pontos ou '
               'sublinhados')])
    password = PasswordField('Senha', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirme a Senha', validators=[DataRequired()])
    tipo_usuario = SelectField('Tipo Usuário', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(1, 64)])
    estado = SelectField('Estado', validators=[DataRequired()], choices=[])
    # cidade = SelectField('Cidade', choices=[], validate=False)
    cidade = NonValidatingSelectField('Cidade', choices=[], validators=[DataRequired()])
    bairro = StringField('Bairro', validators=[DataRequired(), Length(1, 64)])
    rua = StringField('Rua', validators=[DataRequired(), Length(1, 64)])
    complemento = StringField('Complemento', validators=[Optional(), Length(1, 64)])
    numero = StringField('Número', validators=[Optional(), Length(1, 10)])
    telefone1 = StringField('Telefone 1', validators=[DataRequired(), Length(1, 20)])
    telefone2 = StringField('Telefone 2', validators=[Optional(), Length(1, 20)])
    dataNascimento = DateField('Data Nascimento', format='%d/%m/%Y', validators=[Optional()])
    instagram = StringField('Instagram', validators=[Optional(), Length(1, 64)])
    facebook = StringField('Facebook', validators=[Optional(), Length(1, 64)])
    usuario = SelectField('Usuário', choices=[])
    submit = SubmitField('Registrar')