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
)

routes = (
    (RegisterSuggesterResource, "/register/"),
    (LoginSuggesterResource, "/login/base_user/"),
    (LoginAdministratorResource, "/login/admin/"),
    (SuggestionListCreateResource, "/suggesters/suggestions/"),
    (SuggestionListGetAllResource, "/users_suggestions/"),
    (UploadSuggestionResource, "/admins/suggestions/<int:id>/upload/"),
    (RejectSuggestionResource, "/admins/suggestions/<int:id>/reject/"),
)
