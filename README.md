TasksAPI

1. The API is written in Django with Rest Framework.
2. To setup
3. Create a python3 virtual machine with the needed requirements
    3.1. python3 -m virtualenv api
    3.2. pip install django
    3.3. pip install pip install djangorestframework

4. Extract Zip file and open cd into the folder

5. Run API
    5.1. python manage.py runserver
    5.2. Login to API with these following options:
        5.2.1 http://127.0.0.1:8000/list_nc/        #Display of lists with non complete tasks
        5.2.2 http://127.0.0.1:8000/list_c/         #Display of lists with complete tasks
        5.2.3 http://127.0.0.1:8000/list_all/       #Display of lists with all tasks
        5.2.4 http://127.0.0.1:8000/task/           #Show all tasks


    *The interface can be change from HTML to JSON by adding ".json" to the end #Example http://127.0.0.1:8000/task.json

6. To enter Data: Post

{
	"List": [{
		"title": "example list",
		"tasks": [{
			"name": "buy x"},
           {"name": "buy y"
		}]

	}]
}


7. To add tasks:

{
	"ADDTASKS": [{
		"slug": "example-list",
		"tasks": [{
			"name": "buy x1"},
			{"name": "buy y2"
		}]

	}]
}

8. To delete tasks

{
	"DELTASKS": [{
		"slug": "example-list",
		"tasks": [{
			"slug": "buy-x1"},
			{"slug": "buy-y2"
		}]

	}]
}

9. Each list and tasks can be update and delete directly by using its key

