"""Form widget for py_cui. Allows for giving user several fillable text fields in one block
"""

from typing import Any, Callable, Dict, List, Optional, Tuple
import py_cui.ui
import py_cui.widgets
import py_cui.popups


class DuplicateFormKeyError(Exception):
    """Error thrown when a duplicate form field key is passed
    """

    pass


class FormField(py_cui.ui.TextBoxImplementation):
    """Class containing basic logic of a field in a form

    Attributes
    ----------
    _fieldname : str
        Title of the field
    _required : bool
        Toggle for making the field be required
    """

    def __init__(self, fieldname: str, initial_text: str, password: bool, required: bool, logger):
        """Initializer for base FormFields
        """

        super().__init__(initial_text, password, logger)
        self._fieldname = fieldname
        self._required = required


    def get_fieldname(self) -> str:
        """Getter for field name

        Returns
        -------
        fieldname : str
            Title of the field
        """

        return self._fieldname


    def is_valid(self) -> Tuple[bool,Optional[str]]:
        """Function that checks if field is valid.

        This function can be implemented by subclasses to support different
        field types (ex. emails etc.)

        Returns
        -------
        is_valid : bool
            True of valid conditions are met, false otherwise
        msg : str
            Message explaining problem. None if valid
        """

        msg = None
        if len(self._text) == 0 and self.is_required():
            msg = f'Field <{self.get_fieldname()}> cannot be empty!'

        return msg is None, msg


    def is_required(self) -> bool:
        """Checks if field is required

        Returns
        -------
        required : bool
            True if required, false otherwise
        """

        return self._required


class FormFieldElement(py_cui.ui.UIElement, FormField):
    """Extension of UI element representing an individual field in the form

    Attributes
    ----------
    _field_index : int
        The index of the field in the form
    _parent_form : FormPopup / Form
        The parent UI Element that contains the form element
    """

    def __init__(self, parent_form, field_index: int, field, init_text: str, passwd: bool, required: bool, renderer: 'py_cui.renderer.Renderer', logger):
        """Initializer for the FormFieldElement class
        """

        self._parent_form = parent_form
        self._field_index = field_index
        py_cui.ui.UIElement.__init__(self, 0, field, renderer, logger)
        FormField.__init__(self, field, init_text, passwd, required, logger)
        self._help_text = 'Press Tab to move to the next field, or Enter to submit.'
        self._padx = 0
        self._pady = 0
        self._selected = False
        self.update_height_width()


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute start position

        Returns
        -------
        field_start_x, field_start_y : int, int
            The position in characters in the terminal window to start the Field element
        """

        container_height, _ = self._parent_form.get_absolute_dimensions()
        single_field_height = int((container_height - 1 - self._parent_form._pady) / self._parent_form.get_num_fields())
        parent_start_x, parent_start_y = self._parent_form.get_start_position()
        field_start_x = (parent_start_x + 3 + self._parent_form._padx)
        field_start_y = (parent_start_y + 1 + self._parent_form._pady + (single_field_height * self._field_index))
        return field_start_x, field_start_y


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base function. Uses the parent element do compute stop position

        Returns
        -------
        field_stop_x, field_stop_y : int, int
            The position in characters in the terminal window to stop the Field element
        """

        container_height, _ = self._parent_form.get_absolute_dimensions()
        single_field_height = int((container_height - 1 - self._parent_form._pady) / self._parent_form.get_num_fields())
        _, parent_start_y = self._parent_form.get_start_position()
        parent_stop_x, _ = self._parent_form.get_stop_position()
        field_stop_x = (parent_stop_x - 3 - self._parent_form._padx)
        field_stop_y = (parent_start_y + 1 + self._parent_form._pady + (single_field_height * (self._field_index + 1)) -1)
        return field_stop_x, field_stop_y


    def update_height_width(self) -> None:
        """Override of base class. Updates text field variables for form field
        """

        super().update_height_width()
        padx, pady              = self.get_padding()
        start_x, start_y        = self.get_start_position()
        height, width           = self.get_absolute_dimensions()
        self._cursor_text_pos   = 0
        self._cursor_x          = start_x + 2 + padx
        self._cursor_max_left   = self._cursor_x
        self._cursor_max_right  = start_x + width - 1 - pady
        self._cursor_y          = start_y + int(height / 2) + 1
        self._viewport_width    = self._cursor_max_right - self._cursor_max_left


    def _handle_key_press(self, key_pressed: int) -> None:
        """Handles text input for the field. Called by parent
        """

        if key_pressed == py_cui.keys.KEY_LEFT_ARROW:
            self._move_left()
        elif key_pressed == py_cui.keys.KEY_RIGHT_ARROW:
            self._move_right()
        elif key_pressed in py_cui.keys.KEYS_BACKSPACE:
            self._erase_char()
        elif key_pressed == py_cui.keys.KEY_DELETE:
            self._delete_char()
        elif key_pressed == py_cui.keys.KEY_HOME:
            self._jump_to_start()
        elif key_pressed == py_cui.keys.KEY_END:
            self._jump_to_end()
        elif key_pressed > 31 and key_pressed < 128:
            self._insert_char(key_pressed)


    def _draw(self) -> None:
        """Draw function for the field. Called from parent. Essentially the same as a TextboxPopup
        """

        self._renderer.set_color_mode(self._parent_form._color)
        self._renderer.set_color_rules([])
        self._renderer.draw_text(self, self._title, self._cursor_y - 2, bordered=False, selected=self._selected)
        self._renderer.draw_border(self, fill=False, with_title=False)
        render_text = self._text
        if len(self._text) >self._viewport_width:
            end = len(self._text) - (self._viewport_width)
            if self._cursor_text_pos < end:
                render_text = self._text[self._cursor_text_pos:self._cursor_text_pos + (self._viewport_width)]
            else:
                render_text = self._text[end:]
        if self._password:
            temp = '*' * len(render_text)
            render_text = temp
        self._renderer.draw_text(self, render_text, self._cursor_y, selected=self._selected)

        if self._selected:
            self._renderer.draw_cursor(self._cursor_y, self._cursor_x)
        else:
            self._renderer.reset_cursor(self, fill=False)
        self._renderer.unset_color_mode(self._color)


class FormImplementation(py_cui.ui.UIImplementation):
    """Main implementation class for the form widget/popup

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
    """

    def __init__(self, field_implementations: List['FormField'], required_fields: List[str], logger):
        """Initializer for the FormImplemnentation class
        """

        super().__init__(logger)
        self._form_fields = field_implementations
        self._required_fields = required_fields

        self._selected_form_index = 0
        self._on_submit_action: Optional[Callable[[],Any]] = None


    def get_selected_form_index(self) -> int:
        """Getter for selected form index

        Returns
        -------
        selected_form_index : int
            the index of currently selected field
        """

        return self._selected_form_index

    def set_selected_form_index(self, form_index: int) -> None:
        """Setter for selected form index

        Parameters
        ----------
        selected_form_index : int
            the index of the new selected field
        """

        self._selected_form_index = form_index


    def set_on_submit_action(self, on_submit_action: Callable[[],Any]):
        """Setter for callback on submit

        Parameters
        ----------
        on_submit_action : no-arg or lambda function
            Function fired when user 'submits' form
        """

        self._on_submit_action = on_submit_action


    def jump_to_next_field(self) -> None:
        """Function used to jump between form fields
        """

        if self.get_selected_form_index() < (len(self._form_fields) - 1):
            self.set_selected_form_index(self.get_selected_form_index() + 1)
        else:
            self.set_selected_form_index(0)


    def is_submission_valid(self) -> Tuple[bool,Optional[str]]:
        """Function that checks if all fields are filled out correctly

        Returns
        -------
        is_valid : bool
            True of valid conditions are met, false otherwise
        msg : str
            Message explaining problem. None if valid
        """

        for form_field in self._form_fields:
            valid, err_msg = form_field.is_valid()
            if not valid:
                return False, err_msg
        return True, None


    def get(self) -> Dict[str,str]:
        """Gets values entered into field as a dictionary

        Returns
        -------
        field_entries : dict
            A dictionary mapping field names to user inputs
        """

        output = {}
        for form_field in self._form_fields:
            output[form_field.get_fieldname()] = form_field.get()
        return output


class Form(py_cui.widgets.Widget, FormImplementation):
    """Main Widget class extending the FormImplementation. TODO
    """

    pass


class InternalFormPopup(py_cui.popups.MessagePopup):
    """A helper class for abstracting a message popup tied to a parent popup

    Attributes
    ----------
    parent : FormPopup
        The parent form popup that spawned the message popup
    """

    def __init__(self, parent: 'FormPopup', *args):
        """Initializer for Internal form Popup
        """

        super().__init__(*args)
        self._parent = parent


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class, close in parent instead of root
        """

        if key_pressed in self._close_keys:
            self._parent._internal_popup = None


class FormPopup(py_cui.popups.Popup, FormImplementation):
    """Main Popup extension class for forms.

    Attributes
    ----------
    num_fields : int
        Number of fields added to form
    form_fields : List[FormFieldElement]
        individual form field ui element objects
    internal_popup : InternalFormPopup
        A popup spawned in the event of an invalid submission
    """

    def __init__(self, root, fields, passwd_fields, required_fields, fields_init_text, title, color, renderer, logger):

        self._num_fields = len(fields)
        if self._num_fields != len(set(fields)):
            raise DuplicateFormKeyError('PyCUI forms cannot have duplicate fields.')

        py_cui.popups.Popup.__init__(self, root, title, '', color, renderer, logger)

        self._form_fields: List['FormFieldElement'] = []
        for i, field in enumerate(fields):
            init_text = ''
            if field in fields_init_text:
                init_text = fields_init_text[field]
            self._form_fields.append(FormFieldElement(self,
                                              i,
                                              field,
                                              init_text,
                                              (field in passwd_fields),
                                              (field in required_fields),
                                              renderer,
                                              logger))
        self._form_fields[0].set_selected(True)
        FormImplementation.__init__(self, self._form_fields, required_fields, logger)

        self._internal_popup = None


    def get_num_fields(self) -> int:
        """Getter for number of fields

        Returns
        -------
        num_fields : int
            Number of fields in form
        """

        return self._num_fields


    def get_absolute_start_pos(self) -> Tuple[int,int]:
        """Override of base class, computes position based on root dimensions

        Returns
        -------
        start_x, start_y : int
            The coords of the upper-left corner of the popup
        """

        root_height, root_width = self._root.get_absolute_size()

        min_required_x = 80
        if root_width < 80:
            min_required_x = root_width - 6

        min_required_y = 4 + (2 * self._pady) + 5 * self._num_fields
        if root_height < min_required_y:
            min_required_y = root_height

        form_start_x = int(root_width / 2) - int(min_required_x / 2)

        form_start_y = int(root_height / 2) - int(min_required_y / 2)

        return form_start_x, form_start_y


    def get_absolute_stop_pos(self) -> Tuple[int,int]:
        """Override of base class, computes position based on root dimensions

        Returns
        -------
        stop_x, stop_y : int
            The coords of the lower-right corner of the popup
        """

        root_height, root_width = self._root.get_absolute_size()

        min_required_x = 80
        if root_width < 80:
            min_required_x = root_width - 6

        min_required_y = 4 + (2 * self._pady) + 5 * self._num_fields
        if root_height < min_required_y:
            min_required_y = root_height

        form_stop_x = int(root_width / 2) + int(min_required_x / 2)

        form_stop_y = int(root_height / 2) + int(min_required_y / 2)

        return form_stop_x, form_stop_y


    def update_height_width(self) -> None:
        """Override of base class function

        Also updates all form field elements in the form
        """

        super().update_height_width()
        try:
            for element in self._form_fields:
                element.update_height_width()
        except AttributeError:
            pass


    def _handle_key_press(self, key_pressed: int) -> None:
        """Override of base class. Here, we handle tabs, enters, and escapes

        All other key presses are passed to the currently selected field element

        Parameters
        ----------
        key_pressed : int
            Key code of pressed key
        """

        if self._internal_popup is None:
            if key_pressed == py_cui.keys.KEY_TAB:
                self._form_fields[self.get_selected_form_index()].set_selected(False)
                self.jump_to_next_field()
                self._form_fields[self.get_selected_form_index()].set_selected(True)
            elif key_pressed == py_cui.keys.KEY_ENTER:
                valid, err_msg = self.is_submission_valid()
                if valid:
                    self._root.close_popup()
                    if self._on_submit_action is not None:
                        self._on_submit_action(self.get())
                else:
                    self._internal_popup = InternalFormPopup(self,
                                                             self._root,
                                                             err_msg,
                                                             f'Required fields: {str(self._required_fields)}',
                                                             py_cui.YELLOW_ON_BLACK,
                                                             self._renderer,
                                                             self._logger)
            elif key_pressed == py_cui.keys.KEY_ESCAPE:
                self._root.close_popup()
            else:
                if self.get_selected_form_index() < len(self._form_fields):
                    self._form_fields[self.get_selected_form_index()]._handle_key_press(key_pressed)
        else:
            self._internal_popup._handle_key_press(key_pressed)


    def _handle_mouse_press(self, x: int, y: int, mouse_event: int) -> None:
        """Override of base class function

        Simply enters the appropriate field when mouse is pressed on it

        Parameters
        ----------
        x, y : int, int
            Coordinates of the mouse press
        """

        py_cui.popups.Popup._handle_mouse_press(self, x, y, mouse_event)
        for i, field in enumerate(self._form_fields):
            if field._contains_position(x, y):
                self._form_fields[self.get_selected_form_index()].set_selected(False)
                self.set_selected_form_index(i)
                self._form_fields[self.get_selected_form_index()].set_selected(True)
                break


    def _draw(self) -> None:
        """Override of base class.

        Here, we only draw a border, and then the individual form elements
        """

        self._renderer.set_color_mode(self._color)
        self._renderer.set_color_rules([])
        self._renderer.draw_border(self)

        for i, form_field in enumerate(self._form_fields):
            if i != self.get_selected_form_index():
                form_field._draw()

        self._form_fields[self.get_selected_form_index()]._draw()

        if self._internal_popup is not None:
            self._internal_popup._draw()
