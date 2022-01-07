# Easy-Home
## REST-api

* House rent startup
* Owner can add rent details along with multiple image and features
* Authenticated user can create, edit, delete and also save product as a favourite
* Admin support with django built in admin interface (customed) 
* Search, filter functionality for theservice
* Tools–Python3.8, Django, Django Rest Framework, Postgres, Djoser, JWT,
<!-- * demo b-kash payment integrated -->


# Schema
![alt text](home.png?raw=true)

# install
create a virtual environment and activate (virtualenv recomended)
> pip install -r requirements.txt

### build:
>python manage.py runserver



* **Sample Call:**

    ```
    http://127.0.0.1:8000/admin/
    ```

    ```
    http://127.0.0.1:8000/auth/users/
    ```

    ```
    http://127.0.0.1:8000/auth/jwt/create/
    ```

    ```
    http://127.0.0.1:8000/profile
    ```
    
    ```
    http://127.0.0.1:8000/dashboard
    ```
    
    ```
    http://127.0.0.1:8000/advertisement
    ```

    ```
    http://127.0.0.1:8000/advertisement/create
    ```

    ```
    http://127.0.0.1:8000/advertisement/create/<int:id>
    ```
    
    ```
    http://127.0.0.1:8000/favourite
    ```
    
    ```
    http://127.0.0.1:8000/profile/favourite/create
    ```
    
    ```
    http://127.0.0.1:8000/favourite/<int:id>
    ```
