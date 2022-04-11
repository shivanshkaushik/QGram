# Qgram


![image](https://user-images.githubusercontent.com/102377195/162683378-85597c65-ff23-45b4-b43b-4d2617858af0.png)


An App where each person can get a quote for every mood or even any random quote. As the craze of social media increasing, every every person seeks for a perfect quote for themselfs, rather it be for an instagram post or a tweet.
Qgram is here for the rescue !!!

Qgram API users will also have the ability to create, read and delete quotes in database.


# Table of Content


- About
- System Architecture
- Backend
  - Cloud
  - CRUD Operations
    - CRUD Operations in Detail
 - Desclaimer
 
 
# About
**Introduction of cloud application**

Clouds are computing resources for rent. There are many cloud providers to choose from. Some of the main cloud providers are: (Amazon) AWS, (Microsoft) Azure, Google Cloud, IBM Cloud, Alibaba Cloud, Salesforce, Rackspace, Oracle Cloud.

A cloude application is internet-based software that processes or stores data online

There are three main kinds of application:

1. Software as a service
2. Platform as a service
3. Infrastructure as a service


**About Qgram**


Qgram is an api platform where every person can visit and search for a quote according to their moods or feelings. One can also search for their faviorite author. Registered users can also creat their own quotes and can also delete as well if they feel like it.


# System Architecture

![image](https://user-images.githubusercontent.com/102377195/162663991-f9a6677a-78ab-436b-a71d-5b9fc730a0e2.png)


The front-end serves as a seamless user interface for many devices such as smartphones, PCs or laptops. The backend uses REST-based services interface for CRUD operations, such as finding a quote by catagory, getting all quotes, names of author, user sign in and even deleting one with authority. This is deployed via Google cloud with quick response to any request. An attempt to connecting it to a external translating API is also made.

# Backend

Most of the CRUD operations are performed in terminals and browser. One can also make use of Postman for these API's operation.


**CRUD OPERATION**

We will be using the Basic CRUD operations which are possible by accessing the API. One can access these operations via adding ```api/all_author``` and ```api/all_records``` at the end of the web address following the REST standards.

where one can get whole records of data or even a specific result such as,

```{"quote" = "One life, live it!"} ```



# Cloud

Our current backend is deployed on the google cloude. [Click Here](https://github.com/shivanshkaushik/QGram) for details on the API and updates.


**Deploying Qgram to Cloud**

First one have to create a Virtual instance, for which we will need an Google Cloude with proper configurations. 


For a google cloud service,

Sign in/up [here] (https://cloud.google.com).

![image](https://user-images.githubusercontent.com/102377195/162682447-4c27ea4b-b8ea-49b9-9308-bdbd1132c5b8.png)


After Creating an instance, Connect a terminal to it using Linux operating system. SSH (Secure Shell) Protocol will be used here. To do this one will need  public and private keys. We will put the Public Key in the GCP instance. And we will keep the private key on our own PC to connect to the instance in GCP. 

After successfully connecting the cloud, in the next step can we can deploy our application manually or get the respiratory from github. Our main application will be run and in the codes a specific Port is assigned to it.

In our case, we require port 5000, as we have assigned our API to it.

```app.run(host='0.0.0.0', port = 5000)```

We can run the application on the port, using the command :

```python3 (APP_NAME).py```

To verify that the services are running , we will load the external IP with port :

```http://34.89.29.79:5000/```

If it is successful we can access our API and run operations

# CRUD Operations in Detail

A basic overview of CRUD operations 

GET : method is for retrieving information. Our app simply returns the results of some simple data.

POST : allow our clients to remotely add/create new resources.

PUT : allows the user to update their quote data.

DELETE : enables the user to delete their quotes.



**Running Locally**

To run this repository on your local machine download the source code and extract its contents or clone the repository.


Explaining few of the CRUD Operation:

**GET Operation :**

Get method to view all quotes
```
@app.route('/', methods=['GET'])
def get_all_records():

```

Connect to the database
```
cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                      host='35.246.14.186',
                                      database='QGram-db')

```

Error returned if database fails to connect
```
return '{"status":"Database Connection Error","message":"'+str(e)+'"}', 500, {'Content-Type': 'text/json; charset=utf-8'}
    query = "SELECT * FROM quotes_table"

```

execute select query to retrieve all quotes from cloud database
```
cursor.execute(query)
    except Exception as e:

```

Fetching records from the cursor objects
```
records = cursor.fetchall()

```

return error if no quotes found
```
if len(records)==0:
        return '{"status":"No Records Found","message":""}', 404, {
            'Content-Type': 'text/json; charset=utf-8'}
    records_json="["
    for record in records:
        quote=str(record[1])

```

Building output json with all records
```
records_json=records_json+'{"Quote_id":"'+str(record[0])+'","Quote":"'+quote+'","Authors":"'+str(record[2])+'","Category":"'+str(record[3])+'"}'
        if record!=records[-1]:
            records_json=records_json+','
    records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
          'Content-Type': 'text/json; charset=utf-8'}

```

Closing db connection
```
cnx.close()
        except Exception as e:


```

Returning error if closing connection fails
```
return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
 

```

Returning records in the json format
```
return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

```

This will return all the records available in our database.


**More of the GET logics/operation used :**

To Get the list of all the Author :
```
@app.route('/all_authors/', methods=['GET'])
def get_authors():


```


```
records = cursor.fetchall()
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
            'Content-Type': 'text/json; charset=utf-8'}
    records_json=''
    for record in records:
        records_json = records_json + '{"Author":"' + str(record[0]) + '"}'
        if record != records[-1]:
            records_json = records_json + ','
            records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}

```



To get list of Quotes by Author name :
```
@app.route('/quote_by_authors/<author_name>/', methods=['GET'])
def get_quote_by_author(author_name=''):
  author_name=author_name.strip()
  try:
    if author_name =='':
        return '{"status":"No Input Entered","message":""}', 400, {
            'Content-Type': 'text/json; charset=utf-8'}
 except Exception as e:
  return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}

```


**POST OPERATION**

To Post a quote in the Database :

```
@app.route('/update_quote_by_id/', methods=['POST'])
def update_quote_by_id():
  if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
      if request.json["quote_id"] is None or not request.json["quote_id"] and request.json["quote"] is None or not request.json["quote"]:
          return '{"status":"Required Parameter Missing","message":""}', 400, {
              'Content-Type': 'text/json; charset=utf-8'}

```

we will connect to the database similarly as we did in the GET operation
This will 


**PUT OPERATION** 

To Update any existing entry :

```
@app.route('/update_quote_by_id/<id>/<t_lang>', methods=['GET'])
def translate(id,t_lang):
if len(records) == 0:
            return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
        response = requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+t_lang+"&dt=t&q='"+records[0][0]+"'")
        resp_json=response.json()
        return str('{"Quote":"'+records[0][0]+'","language":"'+t_lang+'","translation":"'+resp_json[0][0][0]+'"}'), 200, {'Content-Type': 'text/json; charset=utf-8'}
    except BaseException as be:
        return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}

```




# Disclaimer


This project is part of a cloud computing coursework taught by Dr. Sukhpal Singh Gill at the Queen Mary University of London Electrical Engineering & Computer Science Department to create a prototype of a cloud application.
