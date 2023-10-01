This is serving to explain what the branch should contain up to for when I inevitably come back to my project.

Branch:
virtual-environment-setup 
-> contains up to and only the created virtual environment and the basic set up so being able to run the server.
CRUD-Ops-without-MethodView
-> making initial CRUD options without using MethodView. This has completed routes for user and item routes.
CRUD-Ops-with-MethodView
-> converted initial CRUD operations to work with MethodView
Incorporating-Schemas-Models
-> adding blueprints that can be added as decorators to routes. These take in schemas which works to validate info by making sure any info that is set to required is being given in order to run the function. It also determines which information is only taken and which information is only given. Set up models for user and items that help create the table and columns. Also includes methods for each. Connected to elephantsql database as well. Then made sure that each route sends to the database.
Many-to-Many-Routes
-> added a many to many route in the form of adding friends. one friend can have many friends. That friend can also have many friends.
access-token-jwt-security
-> added jwt security and generate access tokens. provides extra security for methods and keeps users from deleting or editing things that aren't theirs.