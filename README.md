# University ANS app

## Project Introduction
University Assessment and Suggestion is a Web Application made with Flask RESTful framework. <br/>
My defense project for Web Applications with Flask course at Softuni.

## :pencil: Project Description of functionalities
<details>
<summary> 
    Click here for more info. 
</summary>
  
University ANS app idea is to provide diferrent businesses a chance to track the overall assessment from its consumers.
This app could be helpful to improve our services. Our users can post a suggestion and share UX.
Registered user can rate our service and also post his oppinion/suggestment.
In order to post suggestion, users should upload at least one certificate (to prove that they used our service).
We have 2 roles: base user and admin.
  
<strong> Base User: </strong>
* Can post suggestion. retrieve all the uploaded (accepted by admin) suggestions.
* Can rate our service.
* Can retrieve all the uploaded (accpeted by admin) suggestions.
  
<strong> Admin: </strong>
* Can upload(approve) the pending uploads.
* Can reject the pending uploads.
* Can can delete all rejected uploads from data base.
  
<strong> :pushpin: Restrictions: </strong>
* Guest Vistors (a user who is not Logged-in) are restricted to browse only all of the uploaded(accepted) suggestions.
* Base Visitors (Logged-in users) are restricted to browse all of their uploads or all users uploaded(accepted) suggestions.
* Only admins can update, delete or accept suggestions. 

</details>

## :hammer: Used technologies
<details>
<summary> 
    Click here for more info. 
 </summary>
  
The application is made with Flask RESTful framework.
We have Third Party integrations:
* AWS S3 - service which stores the uploaded certificates in the cloud in order to avoid overloading of our server.
* AWS SES - email service which sends automated emails to the users after certain event (being rejected or accepted)

In order to check all the built-in or third party libraries, you can clone the project and type in the terminal:

``` python
pip install -r requirements.txt
```
  
</details>

## API Endpoints
<details>
<summary> 
    Click here for more info. 
 </summary>
  
 POST http://127.0.0.1:5000/register/ - validate and submit data in db (register resource) <br/>
 POST http://127.0.0.1:5000/login/admin/ - validate role type and log with admin rights (login resource) <br/>
 POST http://127.0.0.1:5000/login/user/ - validate role type and log with base user rights <br/>
 POST http://127.0.0.1:5000/suggesters/suggestions/ - validate input and upload suggestion and assessment <br/>
 PUT http://127.0.0.1:5000/admins/suggestions/6/upload/ - update the upload state to accepted (only admins are permitted) <br/>
 PUT http://127.0.0.1:5000/admins/suggestions/4/reject/ - update the upload state to rejected (only admins are permitted) <br/>
 GET http://127.0.0.1:5000/suggesters/suggestions/ - retrieve all of the uploads for the current logged user <br/>
 GET http://127.0.0.1:5000/users/suggestions/ - retrieve all accepted/uploaded resources (Guest Visitor or Regular user) <br/>
 DELETE http://127.0.0.1:5000/admins/suggestions/rejected/delete/ - Delete all the rejected uploads (only admins are permitted)
</details>

   
## Author Name 
Petar Petrov

## License
This project is licensed with the [MIT license](LICENSE).
