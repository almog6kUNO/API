from .models import List,Task
from rest_framework import generics
from .serializers import ListSerializer, TaskSerializer,ListSerializerFilterNotComplete, \
    ListSerializerFilterComplete,ListSerializer_Slug
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


#Get and Post Class view
class List_List(APIView):
    #Set Serilizer
    ser = ListSerializer

    #Show data
    def get(self, request, format=None):
        list = List.objects.all() # Get all list objects

        serializer = self.ser(list, many=True, context={'request': request}) # Collect data from the serializer

        return Response(serializer.data)

    #Post method
    def post(self, request, format=None):
        # Ensure data entery with support for list of lists
        if not 'List' in request.data and not 'ADDTASKS' in request.data and not 'DELTASKS' in request.data:

            return Response({'Please check JSON string and ensure List is set (check Readme)'},
                            status=status.HTTP_400_BAD_REQUEST) #Return an error message if JSON doesn't contain the right syntax
        if 'List' in request.data: #Create new lists with optional tasks
            for data_post in request.data['List']: #Ensure all lists have the right syntax
                if not "title" in data_post:
                    return Response({"name input is missing"}, status=status.HTTP_400_BAD_REQUEST) #If fail, return an error

            result = [] #Hold serial data
            for data_post in request.data['List']: #Loop over the lists

                serializer = self.ser(data=data_post, context={'request': request}) #Collect data from the serializer

                if serializer.is_valid(): #Ensure data validity
                    tasks_to_save = []  # List to save all of the list
                    if 'tasks' in data_post: #Verify if a list has tasks
                        for task in data_post['tasks']: #Loop over the tasks per list
                            if not 'name' in task: # Ensuring the validity of the tasks, if fail, return an error
                                return Response({'Task initialization error. Ensure "name" is used'},
                                                status=status.HTTP_400_BAD_REQUEST)
                            #Add task to the list
                            tasks_to_save.append(task['name'])

                    serializer.save() # Save the list

                    pkey = List.objects.get(slug = serializer.data['key']) #Get the slug name for the list object

                    for task in tasks_to_save: # populate the tasks in the list object
                        q = Task (list = pkey, name = task)
                        q.save()

                    if 'tasks' in serializer.data: #Show tasks in the results
                        for data_taks in data_post['tasks']: #loop over the tasks
                            serializer.data['tasks'].append(data_taks)

                    result.append(serializer.data) # Add data results for display

                else: #If data is not valud, return error
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Something is wrong

            return Response(result, status=status.HTTP_201_CREATED) #Return Created Succesfully Message

        if 'ADDTASKS' in request.data: #Add tasks to a list
            for data_post in request.data['ADDTASKS']: # Loop over the data to ensure syntax
                if not "slug" in data_post and not 'tasks' in data_post: # If missing slug reference, return error
                    return Response({"slug or tasks input is missing"}, status=status.HTTP_400_BAD_REQUEST)
                if not (List.objects.filter(slug= data_post['slug']).exists()):#Ensure list exists, if not, return error
                    return Response({"List not found. Check if slug exists"}, status=status.HTTP_400_BAD_REQUEST)

                for task in data_post['tasks']: #Ensure all tasks are valid
                    if not 'name' in task:
                        return Response({"Task error in "+data_post['slug']}, status=status.HTTP_400_BAD_REQUEST)

            for data_post in request.data['ADDTASKS']: #If all vaid, populate the lists with tasks
                pkey = List.objects.get(slug= data_post['slug']) #Get the list object
                for task in data_post['tasks']: #populate the tasks in the object
                    t = Task(list=pkey, name=task['name'])
                    t.save()

            return Response({"ADDED TASKS!"}, status=status.HTTP_201_CREATED) #return success

        if 'DELTASKS' in request.data: #Delete tasks from an list
            for data_post in request.data['DELTASKS']: #Ensure data validity
                if not "slug" in data_post and not 'tasks' in data_post: #Ensure slug data is present, else return an error
                    return Response({"slug or tasks input is missing"}, status=status.HTTP_400_BAD_REQUEST)
                if not (List.objects.filter(slug= data_post['slug']).exists()): #Ensure slug objects exist, else, return error
                    return Response({"List not found. Check if slug exists"}, status=status.HTTP_400_BAD_REQUEST)

                for task in data_post['tasks']: #Ensure all data slug is valid, else return error
                    if not 'slug' in task:
                        return Response({"Task error in "+data_post['slug']}, status=status.HTTP_400_BAD_REQUEST)

            for data_post in request.data['DELTASKS']: #if all valid, delete tasks
                pkey = List.objects.get(slug= data_post['slug']) # Get list object
                for task in data_post['tasks']: #Delete
                    t = Task.objects.get(list = pkey, slug = task['slug'])
                    t.delete()

            return Response({"Delete OK!"}, status=status.HTTP_200_OK)


#inhertaince from List to show only Not Complete
class List_Not_Complete_List(List_List):

    ser = ListSerializerFilterNotComplete #Get only not complete data

class List_Complete_List(List_List):

    ser = ListSerializerFilterComplete #Get only complete data



#Show details about a single List (Showing all)
class List_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer_Slug #Get data from the serializer
    lookup_field = 'slug' #Use slug to locate and build URL for the list

#Showing all of the tasks
class Task_List(generics.ListCreateAPIView):
    queryset = Task.objects.all() #Get all tasks objects
    serializer_class = TaskSerializer #Get data from the serializer
    lookup_field = 'slug'

#Showing detail of a task
class Task_Detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all() #Get all tasks objects
    serializer_class = TaskSerializer #Get data from the serializer
    lookup_field = 'slug' #Use slug to locate and build URL for the task
