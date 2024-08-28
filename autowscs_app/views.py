import faulthandler
from django.shortcuts import render, redirect
from .models import Webservicelist, Parameterlist, Inputparameter, Outputparameter, ParameterHierarchy, Result, Initialgoalparameter
import random
# Create your views here.


def index(request):
    webservicelist = Webservicelist.objects.all()
    parameterlist = Parameterlist.objects.all()
    inputparameterlist = Inputparameter.objects.all()
    outputparameterlist = Outputparameter.objects.all()
    parameterhierarchy = ParameterHierarchy.objects.all()
    result = Result.objects.all()
    parent_parameters = parameterhierarchy.values_list('parentParameterID', flat=True).distinct()
    parent_parameters_list = list(parent_parameters)
    child_parameters = parameterhierarchy.values_list('childParameterID', flat=True).distinct()
    child_parameters_list = list(child_parameters)
    context = {
        'webservicelist':webservicelist,
        'parameterlist':parameterlist,
        'inputparameterlist':inputparameterlist,
        'outputparameterlist':outputparameterlist,
        'parameterhierarchy_list':parameterhierarchy,
        'parent_parameters':parent_parameters_list,
        'child_parameters':child_parameters_list,
    }
    return render(request, 'edit_database.html', context)

             
def add_webservice(request):

    if request.method == 'POST':
        webserviceid = request.POST.get('webserviceid')
        webservice_name = request.POST.get('webservicename')
        reputation = request.POST.get('reputation')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        provider = request.POST.get('provider')
        webservice_url = request.POST.get('webservice_url')

        Webservicelist.objects.update_or_create(
            webserviceid=webserviceid,
            defaults={
                "webserviceid": webserviceid,
                "name": webservice_name,
                "reputation": reputation,
                "price": price,
                "duration": duration,
                "provider": provider,
                "url": webservice_url
            }
        )
        return redirect('/')
    
    display_message = "Webservice added successfully"
    context = {'display_message':display_message}
    return render(request, 'edit_database.html', context)


def delete_webservice(request):

    if request.method == 'POST':
        webserviceid = request.POST.get('webservice_delete')
        Webservicelist.objects.get(pk=webserviceid).delete()
        display_message = "Deleted Webservice successfully"
        context = {
            'display_message':display_message,
        }
        return redirect('/', context)
    
    display_message = "Deleted Webservice successfully"
    context = {
        'display_message':display_message,
    }
    return render(request, 'edit_database.html', context)

def add_parameter(request):

    if request.method == 'POST':
        parameterid = request.POST.get('parameterid')
        parameter_name = request.POST.get('parameter_name')

        Parameterlist.objects.update_or_create(
            parameterid=parameterid,
            defaults={
                "parameterid": parameterid,
                "name": parameter_name
            }
        )
        return redirect('/#edit_knowledge')
    
    display_message = "Parameter added successfully"
    context = {'display_message':display_message}
    return render(request, 'edit_database.html', context)

def delete_parameter(request):

    if request.method == 'POST':
        parameterid = request.POST.get('parameter_delete')
        Parameterlist.objects.get(pk=parameterid).delete()
        display_message = "Deleted parameter successfully"
        context = {
            'display_message':display_message,
        }
        return redirect('/', context)
    
    display_message = "Deleted parameter successfully"
    context = {
        'display_message':display_message,
    }
    return render(request, 'edit_database.html', context)


def add_inputparameter(request):

    if request.method == 'POST':
        parameterid = request.POST.get('parameterid')
        webserviceid = request.POST.get('webserviceid')

        Inputparameter.objects.update_or_create(
            parameterid=parameterid,
            defaults={
                "parameterid": parameterid,
                "webserviceid": webserviceid
            }
        )
        return redirect('/')
    
    display_message = "InputParameter added successfully"
    context = {'display_message':display_message}
    return render(request, 'edit_database.html', context)

def delete_inputparameter(request):

    if request.method == 'POST':
        parameterid = request.POST.get('inputparameter_delete')
        Parameterlist.objects.get(pk=parameterid).delete()
        display_message = "Deleted input parameter successfully"
        context = {
            'display_message':display_message,
        }
        return redirect('/', context)
    
    display_message = "Deleted input parameter successfully"
    context = {
        'display_message':display_message,
    }
    return render(request, 'edit_database.html', context)


# def add_pre_or_post_knowledge(request, knowledgeTable, course_str, knowl_str, err_prompt, bitmask):
#         if request.method == 'POST':
#             webserviceid = request.POST.get(course_str)
#             webservice = Webservicelist.objects.get(pk=webserviceid)
#             parameterid = request.POST.get(knowl_str)
#             parameter = Parameterlist.objects.get(pk=parameterid)
#             # check initial and goal are different
#             knowledgeTable.objects.update_or_create(
#                 courseid=pre_course,
#                 knowledgeid=pre_know,
#                 defaults={
#                     "courseid": pre_course,
#                     "knowledgeid": pre_know
#                 }
#             )

#     except Exception as e :
#         display_message = "Unable to add the " + err_prompt + "." + repr(e)
#         Aplogger.get_instance().log_message(display_message, Logenum.error)

#     finally:
#         context = get_context_for_edit_database(bitmask, display_message)
#         return render(request, 'po/edit-database.html', context)


def parameterhierarchy(request):
    if request.method == 'POST':
        parentParameterID = request.POST.get('parentParameterID')
        childParameterID = request.POST.get('childParameterID')
        noOfDepth = request.POST.get('noOfDepth')
        noOfChildren = request.POST.get('noOfChildren')
        ParameterHierarchy.objects.create(
            parentParameterID = parentParameterID,
            childParameterID=childParameterID,
            noOfDepth=noOfDepth,
            noOfChildren=noOfChildren
        )
        return redirect('/#hierarchy')
    display_message = "parameterhierarchy added successfully"
    context = {
        'display_message':display_message,
    }
    return render(request, 'edit_database.html', context)

from django.http import JsonResponse

def parameterhierarchy_data(request):
    data = list(ParameterHierarchy.objects.filter(noOfChildren=2).values().distinct())
    relationship_dict = {}
    data = list(ParameterHierarchy.objects.filter(noOfChildren=2).values())
    separated_data = {}

    # Iterate through the list and populate separated_data
    for item in data:
        parent_id = item['parentParameterID']
        if parent_id in separated_data:
            separated_data[parent_id].append(item)
        else:
            separated_data[parent_id] = [item]

    # Extract the arrays from the separated_data dictionary
    result_arrays = list(separated_data.values())

    relationship_dict = {}
    for item in result_arrays[0]:
        parent_id = item["parentParameterID"]
        child_id = item["childParameterID"]
        if parent_id not in relationship_dict:
            relationship_dict[parent_id] = {"name": parent_id, "children": []}
        current_child = None
        for child in relationship_dict[parent_id]["children"]:
            if child["name"] == child_id:
                current_child = child
                break
        if current_child is None:
            current_child = {"name": child_id, "children": []}
            relationship_dict[parent_id]["children"].append(current_child)
        sub_child_data = ParameterHierarchy.objects.filter(parentParameterID=child_id,noOfChildren=2).values()
        sub_child_data = [{"name": sub_child["childParameterID"]} for sub_child in sub_child_data]
        for sub_child in sub_child_data:
            if len(current_child["children"]) < 2:
                current_child["children"].append(sub_child)
            else:
                relationship_dict[parent_id]["children"].append({"name": child_id, "children": [sub_child]})
                current_child = relationship_dict[parent_id]["children"][-1]

                current_child = relationship_dict[parent_id]["children"][-1]    
    
    response_data = list(relationship_dict.values())

    return JsonResponse(response_data, safe=False)

def org_chart(request):
    return render(request, "grapicalview.html")

def upload_datafile(request):
    parameterlist = Parameterlist.objects.all()
    webservicelist = Webservicelist.objects.all()
    context = {
        'parameterlist': parameterlist,
        'webservicelist': webservicelist,
    }
    return render(request, 'multi-upload.html', context)


# def show_resultt(request):
#     return render(request, 'show_result.html')

def upload_datafile(request):
    parameterlist = Parameterlist.objects.all()
    context = {
        'parameterlist': parameterlist,
    }
    return render(request, 'multi-upload.html', context)

def has_common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if a_set & b_set:
        return True
    else:
        return False
    
    
def write_initialgoalknowledge_to_table(transactID, iknwdList, iiorg):
    aListOfKnowledge = []
    for knwldName in iknwdList:
        knwdListObj = Parameterlist.objects.get(name=knwldName)
        aListOfKnowledge.append(Initialgoalparameter(transactionid=transactID, iorg=iiorg, knowledgeid=knwdListObj))

    Initialgoalparameter.objects.bulk_create(aListOfKnowledge)


def write_initialgoalknowledge_to_table_from_courses(transactID, icourseList, iiorg):
    print("nnnnnn",icourseList,transactID)
    aListOfKnowledge = []
    for courseName in icourseList:
        print("&&&&&", courseName)
        courseListObj = Webservicelist.objects.get(name=courseName)
        print("lklklkl",courseListObj)
        postKnwldObjectList = Inputparameter.objects.filter(webserviceid=courseListObj.webserviceid)
        
        for postKnwldObject in postKnwldObjectList:
            knwdListObj = Parameterlist.objects.get(pk=postKnwldObject.parameterid.parameterid)
            aListOfKnowledge.append(
                Initialgoalparameter(transactionid=transactID, iorg=iiorg, knowledgeid=knwdListObj))

    Initialgoalparameter.objects.bulk_create(aListOfKnowledge)

import random
import subprocess
from django.shortcuts import render
from .models import Initialgoalparameter, Result, Webservicelist  # Adjust model imports as necessary

def show(request):
    return render(request, 'show.html')



def show_result_static(request):
    all_courses = [
    {'stage': 'Stage 1', 'webserviceid': 'WS1', 'name': 'getVacationLocation'},
    {'stage': 'Stage 2', 'webserviceid': 'WS2', 'name': 'getAirlineTicket'},
    # Add more courses as needed
]
    return render(request, 'show.html', {'all_courses': all_courses})

def show_result(request):
    lCourseObj = []
    retVal = False
    if request.method == 'POST':
        initials = request.POST.getlist('initials')
        goals = request.POST.getlist('knowledges')
        depth = request.POST.get('depth')
        child = request.POST.get('child')
        
        if initials and goals:
            if not has_common_member(initials, goals):
                random.seed()
                transactID = random.randint(1, 1000)
                write_knowledge_to_table(transactID, initials, 'I')
                write_knowledge_to_table(transactID, goals, 'G')
                retVal = True
                subprocess.call(['java', '-jar', 'C:\AutoPlan\AutoWSC-AIPSYooMath.jar', str(transactID), depth, child])
                    
                resultList = Result.objects.filter(transactionid=transactID).order_by('stage')
                print(resultList)
                for res in resultList:
                    course = Webservicelist.objects.get(webserviceid=res.webserviceid)
                    course.stage = res.stage
                    lCourseObj.append(course)
            
        if retVal:
            context = {
                'all_courses': lCourseObj,
                'transactionID': transactID
            }
            print(lCourseObj)
            return render(request, 'show_result.html', context)
        else:
            return upload_datafile(request)
    else:
        # Handle non-POST request here
        return upload_datafile(request)

def write_knowledge_to_table(transactID, parameter_ids, iorg):
    """
    Writes knowledge parameters (initials or goals) to the table, fixing the issue where 
    'parameterid' needs to be an instance of 'Parameterlist'.
    
    :param transactID: Unique transaction ID.
    :param parameter_ids: List of parameter IDs or web service IDs.
    :param iorg: 'I' for Initial or 'G' for Goal knowledge.
    """
    for param_id in parameter_ids:
        # Fetch the Parameterlist instance corresponding to the param_id
        parameter_instance = Parameterlist.objects.get(parameterid=param_id)
        
        # Now, use this instance instead of the string for parameterid
        Initialgoalparameter.objects.create(
            transactionid=transactID, 
            iorg=iorg, 
            parameterid=parameter_instance
        )


