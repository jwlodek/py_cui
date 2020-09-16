# form

Form widget for py_cui. Allows for giving user several fillable text fields in one block



#### Classes

 Class  | Doc
-----|-----
 DuplicateFormKeyError(Exception) | Error thrown when a duplicate form field key is passed
 FormField(py_cui.ui.TextBoxImplementation) | Class containing basic logic of a field in a form
 FormFieldElement(py_cui.ui.UIElement, FormField) | Extension of UI element representing an individual field in the form
 FormImplementation(py_cui.ui.UIImplementation) | Main implementation class for the form widget/popup
 Form(py_cui.widgets.Widget, FormImplementation) | Main Widget class extending the FormImplementation. TODO
 InternalFormPopup(py_cui.popups.MessagePopup) | A helper class for abstracting a message popup tied to a parent popup
 FormPopup(py_cui.popups.Popup, FormImplementation) | Main Popup extension class for forms.




## DuplicateFormKeyError(Exception)

```python
class DuplicateFormKeyError(Exception)
```

Error thrown when a duplicate form field key is passed









## FormField(py_cui.ui.TextBoxImplementation)

```python
class FormField(py_cui.ui.TextBoxImplementation)
```

Class containing basic logic of a field in a form




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _fieldname  |  str | Title of the field
 _required  |  bool | Toggle for making the field be required

#### Methods

 Method  | Doc
-----|-----
 get_fieldname | Getter for field name
 is_valid | Function that checks if field is valid.
 is_required | Checks if field is required




### __init__

```python
def __init__(self, fieldname, initial_text, password, required, logger)
```

Initializer for base FormFields







### get_fieldname

```python
def get_fieldname(self)
```

Getter for field name




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 fieldname  |  str | Title of the field





### is_valid

```python
def is_valid(self)
```

Function that checks if field is valid.



This function can be implemented by subclasses to support different
field types (ex. emaile etc.)


#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 is_valid  |  bool | True of valid conditions are met, false otherwise
 msg  |  str | Message explaining problem. None if valid





### is_required

```python
def is_required(self)
```

Checks if field is required




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 required  |  bool | True if required, false otherwise








## FormFieldElement(py_cui.ui.UIElement, FormField)

```python
class FormFieldElement(py_cui.ui.UIElement, FormField)
```

Extension of UI element representing an individual field in the form




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 _field_index  |  int | The index of the field in the form
 _parent_form  |  FormPopup / Form | The parent UI Element that contains the form element

#### Methods

 Method  | Doc
-----|-----
 get_absolute_start_pos | Override of base function. Uses the parent element do compute start position
 get_absolute_stop_pos | Override of base function. Uses the parent element do compute stop position
 update_height_width | Override of base class. Updates text field variables for form field
 _handle_key_press | Handles text input for the field. Called by parent
 _draw | Draw function for the field. Called from parent. Essentially the same as a TextboxPopup




### __init__

```python
def __init__(self, parent_form, field_index, field, init_text, passwd, required, renderer, logger)
```

Initializer for the FormFieldElement class







### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base function. Uses the parent element do compute start position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 field_start_x, field_start_y  |  int, int | The position in characters in the terminal window to start the Field element





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base function. Uses the parent element do compute stop position




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 field_stop_x, field_stop_y  |  int, int | The position in characters in the terminal window to stop the Field element





### update_height_width

```python
def update_height_width(self)
```

Override of base class. Updates text field variables for form field







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Handles text input for the field. Called by parent







### _draw

```python
def _draw(self)
```

Draw function for the field. Called from parent. Essentially the same as a TextboxPopup










## FormImplementation(py_cui.ui.UIImplementation)

```python
class FormImplementation(py_cui.ui.UIImplementation)
```

Main implementation class for the form widget/popup



Attriubutes
-----------
_form_fields : List[FormField]
The current fields in the form
_required_fields : List[str]
List for identifying required fields
_selected_form_index : int
Index of currently selected form
_on_submit_action : no-arg or lambda function
Function fired when submit is called

#### Methods

 Method  | Doc
-----|-----
 get_selected_form_index | Getter for selected form index
 set_selected_form_index | Setter for selected form index
 set_on_submit_action | Setter for callback on submit
 jump_to_next_field | Function used to jump between form fields
 is_submission_valid | Function that checks if all fields are filled out correctly
 get | Gets values entered into field as a dictionary




### __init__

```python
def __init__(self, field_implementations, required_fields, logger)
```

Initializer for the FormImplemnentation class







### get_selected_form_index

```python
def get_selected_form_index(self)
```

Getter for selected form index




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 selected_form_index  |  int | the index of currently selected field





### set_selected_form_index

```python
def set_selected_form_index(self, form_index)
```

Setter for selected form index




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 selected_form_index  |  int | the index of the new selected field





### set_on_submit_action

```python
def set_on_submit_action(self, on_submit_action)
```

Setter for callback on submit




#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 on_submit_action  |  no-arg or lambda function | Function fired when user 'submits' form





### jump_to_next_field

```python
def jump_to_next_field(self)
```

Function used to jump between form fields







### is_submission_valid

```python
def is_submission_valid(self)
```

Function that checks if all fields are filled out correctly




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 is_valid  |  bool | True of valid conditions are met, false otherwise
 msg  |  str | Message explaining problem. None if valid





### get

```python
def get(self)
```

Gets values entered into field as a dictionary




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 field_entries  |  dict | A dictionary mapping field names to user inputs








## Form(py_cui.widgets.Widget, FormImplementation)

```python
class Form(py_cui.widgets.Widget, FormImplementation)
```

Main Widget class extending the FormImplementation. TODO









## InternalFormPopup(py_cui.popups.MessagePopup)

```python
class InternalFormPopup(py_cui.popups.MessagePopup)
```

A helper class for abstracting a message popup tied to a parent popup




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 parent  |  FormPopup | The parent form popup that spawned the message popup

#### Methods

 Method  | Doc
-----|-----
 _handle_key_press | Override of base class, close in parent instead of root




### __init__

```python
def __init__(self, parent, *args)
```

Initializer for Internal form Popup







### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class, close in parent instead of root










## FormPopup(py_cui.popups.Popup, FormImplementation)

```python
class FormPopup(py_cui.popups.Popup, FormImplementation)
```

Main Popup extension class for forms.




#### Attributes

 Attribute  | Type  | Doc
-----|----------|-----
 num_fields  |  int | Number of fields added to form
 form_fields  |  List[FormFieldElement] | individual form field ui element objects
 internal_popup  |  InternalFormPopup | A popup spawned in the event of an invalid submission

#### Methods

 Method  | Doc
-----|-----
 get_num_fields | Getter for number of fields
 get_absolute_start_pos | Override of base class, computes position based on root dimensions
 get_absolute_stop_pos | Override of base class, computes position based on root dimensions
 update_height_width | Override of base class function
 _handle_key_press | Override of base class. Here, we handle tabs, enters, and escapes
 _handle_mouse_press | Override of base class function
 _draw | Override of base class.




### __init__

```python
def __init__(self, root, fields, passwd_fields, required_fields, fields_init_text, title, color, renderer, logger)
```









### get_num_fields

```python
def get_num_fields(self)
```

Getter for number of fields




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 num_fields  |  int | Number of fields in form





### get_absolute_start_pos

```python
def get_absolute_start_pos(self)
```

Override of base class, computes position based on root dimensions




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 start_x, start_y  |  int | The coords of the upper-left corner of the popup





### get_absolute_stop_pos

```python
def get_absolute_stop_pos(self)
```

Override of base class, computes position based on root dimensions




#### Returns

 Return Variable  | Type  | Doc
-----|----------|-----
 stop_x, stop_y  |  int | The coords of the lower-right corner of the popup





### update_height_width

```python
def update_height_width(self)
```

Override of base class function



Also updates all form field elements in the form





### _handle_key_press

```python
def _handle_key_press(self, key_pressed)
```

Override of base class. Here, we handle tabs, enters, and escapes



All other key presses are passed to the currently selected field element


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 key_pressed  |  int | Key code of pressed key





### _handle_mouse_press

```python
def _handle_mouse_press(self, x, y)
```

Override of base class function



Simply enters the appropriate field when mouse is pressed on it


#### Parameters

 Parameter  | Type  | Doc
-----|----------|-----
 x, y  |  int, int | Coordinates of the mouse press





### _draw

```python
def _draw(self)
```

Override of base class.



Here, we only draw a border, and then the individual form elements








