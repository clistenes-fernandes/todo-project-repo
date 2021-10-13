GET_METHOD = 'GET'
POST_METHOD = 'POST'
PUT_METHOD = 'PUT'
DELETE_METHOD = 'DELETE'
CONTENT_TYPE_JSON = 'text/json'
AUTHORIZATION_KEY = 'Authorization'
HS256_ALGORITHM = 'HS256'
SUCCESS_KEY = 'Success'
ERROR_KEY = 'Error'
REMINDER_WRN = 'REMINDER_WARNING'
REMINDER_WRN_MSG = "The due time of this todo will be in {} minute(s)!"
EXPIRED_TODO_REMINDER_MSG = "This todo is expired!"
DATE_FORMAT_STR = '%Y-%m-%d %H:%M'
STATUS_FIELD_DONE = 'D'
STATUS_FIELD_ACTIVE = 'A'
STATUS_FIELD_NONE = 'N'

# Success Messages
SUCCESSFULLY_CREATED_MSG = "Successfully created!"
UPDATED_MSG = "Successfully updated!"
TODO_REMOVED_MSG = "To Do successfully removed!"
USER_REMOVED_MSG = "User successfully removed!"

# Error Messages
TODO_INSERTION_ERROR_MSG = "The Todo could not be inserted"
UPDATE_ERROR_MSG = "Could not update"
TODO_DELETION_ERROR_MSG = "Could not remove the todo, check the 'ToDo' ID"
USER_NOT_FOUND_MSG = "Not possible to retrieve the user"
REQUIRED_FIELDS_ERR0R_MSG = 'Please check and insert all the required fields'
DUE_DATE_ERR0R_MSG = "Due date must be equal or greater then now"
FLAG_NUMBER_ERR0R_MSG = 'The maximum number of flags is 5'
USER_DOES_NOT_EXIST_MSG = 'User matching query does not exist.'
DATE_FORMAT_ERROR_MSG = "The date must be the format: yyyy-mm-dd HH:MM"
WRONG_FIELD_ERROR_MSG = "Field can not be changed {}"
EMPTY_FIELD_ERROR_MSG = "The field %s can not be empty"
USER_DELETION_ERROR_MSG = "The user could not be removed"
NO_TODO_MSG = "No todo with the specified ID"

# MODEL FIELDS
NAME_FIELD = 'name'
DESCRIPTION_FIELD = 'description'
STATUS_FIELD = 'status'
REMINDER_FIELD = 'reminder'
DUE_FIELD = 'due'
FLAGS_FIELD = 'flags'
USER_FIELD = 'user'
ID_FIELD = 'id'
USER_ID_FIELD = 'user_id'
CREATED_FIELD = 'created'
EDITED_FIELD = 'edited'

# USER FIELDS
USER_NAME_FIELD = 'username'
FIRST_NAME_FIELD = 'first_name'
LAST_NAME_FIELD = 'last_name'
EMAIL_FIELD = 'email'
PASSWORD_FIELD = 'password'
