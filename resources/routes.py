from resources.auth import RegisterSuggesterResource, LoginSuggesterResource

routes = ((RegisterSuggesterResource, "/register"), (LoginSuggesterResource, "/signin"))
