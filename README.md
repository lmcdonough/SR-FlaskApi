This is a basic Flask app with a simple api.

Below is the api documentation, I am using curl in my examples.

To receive all messages:
curl http://my-website.com/history/messages/

to receive all messages for a specific user:
curl http://my-website.com/history/Username

to create a new post for a specific user:
curl -H "Content-Type: application/json" -d '{"Title":"Message Title","Message":"This is my message}' -X POST http://mywebsite.com/history/Username

Notes, when posting the title field is required, if you are a posting a message for a new contact, this will automatically create a new contact for you, currently
the contact field in the domain structure cannot handle spaces so use a name like "Julio".