from resources.auth import (
    RegisterSuggesterResource,
    LoginSuggesterResource,
    LoginAdministratorResource,
)
from resources.suggestion import (
    SuggestionListCreateResource,
    UploadSuggestionResource,
    RejectSuggestionResource,
    SuggestionListGetAllResource,
    DeleteRejectedSuggestionsResource,
)

routes = (
    (RegisterSuggesterResource, "/register/"),
    (LoginSuggesterResource, "/login/user/"),
    (LoginAdministratorResource, "/login/admin/"),
    (SuggestionListCreateResource, "/suggesters/suggestions/"),
    (SuggestionListGetAllResource, "/users/suggestions/"),
    (UploadSuggestionResource, "/admins/suggestions/<int:id>/upload/"),
    (RejectSuggestionResource, "/admins/suggestions/<int:id>/reject/"),
    (DeleteRejectedSuggestionsResource, "/admins/suggestions/rejected/delete/"),
)
