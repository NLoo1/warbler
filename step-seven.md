### Step Seven

-   How is the logged in user being kept track of?
>When logging in, the user's id is saved to the Flask session.
-   What is Flask’s _**g**_ object?
> The **g** object allows for data to be stored globally within the app context for continuous usage alongside the Flask session.
-   What is the purpose of _**add_user_to_g ?**_
> Adds logged in user to g and declares that user's data as global within the app context
-   What does _**@app.before_request**_ mean?
> Executes a function before each request is made
