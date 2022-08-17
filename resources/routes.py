from resources.auth import RegisterSuggesterResource, LoginSuggesterResource
from resources.suggestion import SuggestionListCreateResource, UploadSuggestion, RejectSuggestion

routes = ((RegisterSuggesterResource, "/register"),
          (LoginSuggesterResource, "/signin"),
          (SuggestionListCreateResource, "/suggesters/suggestions"),
          (UploadSuggestion, "/admins/suggestions/<int:id>/upload"),
          (RejectSuggestion, "/admins/suggestions/<int:id>/reject")
          )

