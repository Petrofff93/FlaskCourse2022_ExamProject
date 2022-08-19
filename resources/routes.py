from resources.auth import RegisterSuggesterResource, LoginSuggesterResource, LoginAdministratorResource
from resources.suggestion import SuggestionListCreateResource, UploadSuggestion, RejectSuggestion

routes = ((RegisterSuggesterResource, "/register/"),
          (LoginSuggesterResource, "/login/base_user/"),
          (LoginAdministratorResource, "/login/admin/"),
          (SuggestionListCreateResource, "/suggesters/suggestions/"),
          (UploadSuggestion, "/admins/suggestions/<int:id>/upload/"),
          (RejectSuggestion, "/admins/suggestions/<int:id>/reject/")
          )

