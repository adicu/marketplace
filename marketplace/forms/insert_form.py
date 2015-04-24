from wtforms import Form, BooleanField, TextField, SelectField, DecimalField, FileField, validators

class InsertForm(Form):
    name = TextField('Item Name', [validators.Length(min=6, max=200), validators.Required()])
    description = TextField('Description', [validators.Length(min=10, max=2000), validators.Required()])
    condition = SelectField('Condition', [validators.Required()], 
    									  choices=[('new', 'New'), 
    											  ('refurb', 'Mfg. Refurbnished'), 
    											  ('u_mint', 'Used - Mint'),
    											  ('u_vg', 'Used - Very good'),
    											  ('u_good', 'Used - Good'),
    											  ('u_fair', 'Used - Fair'),
    											  ('u_bad', 'Used - Bad')])
    price = DecimalField('Price', [validators.Required()]) 
    image = FileField('Image')  #RegEx (shamelessly?) taken from the docs
    accept_terms = BooleanField('I accept Marketplace\'s terms of service', [validators.Required()])