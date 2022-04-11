#Importing the necessary libraries
import mysql.connector
from flask import Flask, request
import requests

#Start of flask app
app = Flask(__name__)

#get method to view all quotes
@app.route('/', methods=['GET'])
def get_all_records():
  try:
    try:
        # Connect to the database
        cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                      host='35.246.14.186',
                                      database='QGram-db')
        cursor = cnx.cursor()
    except Exception as e:
        #Error returned if database fails to connect
        return '{"status":"Database Connection Error","message":"'+str(e)+'"}', 500, {'Content-Type': 'text/json; charset=utf-8'}
    query = "SELECT * FROM quotes_table"
    try:
        #execute select query to retrieve all quotes from cloud database
        cursor.execute(query)
    except Exception as e:
        #Error returned if query fails to execute
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
    #Fetching records from the cursor objects
    records = cursor.fetchall()
    #return error if no quotes found
    if len(records)==0:
        return '{"status":"No Records Found","message":""}', 404, {
            'Content-Type': 'text/json; charset=utf-8'}
    records_json="["
    for record in records:
        quote=str(record[1])
        #Escaping double quotes
        quote=quote.replace('"','\\"')
        #Building output json with all records
        records_json=records_json+'{"Quote_id":"'+str(record[0])+'","Quote":"'+quote+'","Authors":"'+str(record[2])+'","Category":"'+str(record[3])+'"}'
        if record!=records[-1]:
            records_json=records_json+','
    records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
          'Content-Type': 'text/json; charset=utf-8'}
  finally:
        try:
            #Closing db connection
            cnx.close()
        except Exception as e:
            #Returning error if closing connection fails
            return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
  #Returning records in the json format
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

#Flask GET method to print name of all authors
@app.route('/all_authors/', methods=['GET'])
def get_authors():
  try:
    try:
        # Connect to the database
        cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                      host='35.246.14.186',
                                      database='QGram-db')
        cursor = cnx.cursor()
    except Exception as e:
        # Error returned if database fails to connect
        return '{"status":"Database Connection Error","message":"'+str(e)+'"}', 500, {'Content-Type': 'text/json; charset=utf-8'}
    query="select author from quotes_table";
    try:
        #Executing select query
        cursor.execute(query)
    except Exception as e:
        # Error returned if query fails to execute
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}

    records = cursor.fetchall()
    if len(records) == 0:
        # return error if no quotes found
        return '{"status":"No Records Found","message":""}', 404, {
            'Content-Type': 'text/json; charset=utf-8'}
    records_json=''
    # Building output json with all records
    for record in records:
        records_json = records_json + '{"Author":"' + str(record[0]) + '"}'
        if record != records[-1]:
            records_json = records_json + ','
            records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
      try:
          #closing db connection
          cnx.close()
      except Exception as e:
          # rexception message if connection fails to close
          return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  #returning response if success
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

#GET method to retrieve quotes by a particular author
@app.route('/quote_by_authors/<author_name>/', methods=['GET'])
def get_quote_by_author(author_name=''):
  author_name=author_name.strip()
  try:
      #Return with error if author_name empty
    if author_name =='':
        return '{"status":"No Input Entered","message":""}', 400, {
            'Content-Type': 'text/json; charset=utf-8'}
    try:
        # Connect to the database
        cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                          host='35.246.14.186',
                                          database='QGram-db')
        cursor = cnx.cursor()
    except Exception as e:
        # Exception if database fails  to connect
        return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    #query to get quotes from database by a particular author
    query = "SELECT * FROM quotes_table where author='"+author_name+"'"
    try:
        #Executing select query
        cursor.execute(query)
    except Exception as e:
        #error message returned if query fails to execute
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    if len(records) == 0:
        #Response returned if no records found
        return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
    records_json = "["
    # Building output json with all records
    for record in records:
        quote = str(record[1])
        #Escapiong the double quotes in quote strings
        quote = quote.replace('"', '//"')
        records_json = records_json + '{"Quote_id":"' + str(
            record[0]) + '","Quote":"' + quote + '","Authors":"' + str(record[2]) + '","Category":"' + str(
            record[3]) + '"}'
        if record != records[-1]:
            records_json = records_json + ','
    records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
    try:
        #closing db connection
        cnx.close()
    except Exception as e:
        #Exception message returned if connection fails to close to db
        return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  #Response returned on successful execution of request
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

#POST method to add a quote record to the database
@app.route('/create/', methods=['POST'])
def create_a_quote():
  #Authenticating username and password
  if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
      #Response returned with error if mandatory parameter not present in request
      if request.json["quote"] is None or not request.json["quote"] or request.json["category"] is None or not request.json["category"] or request.json["author"] is None or not request.json["author"]:
          return '{"status":"Required Parameter Missing","message":""}', 400, {
              'Content-Type': 'text/json; charset=utf-8'}
      try:
          try:
            # Connect to the database
               cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                          host='35.246.14.186',
                                          database='QGram-db')
               cursor = cnx.cursor()
          except Exception as e:
          #response returned  if connection to db fails
              return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
          #insert query to create a record of the quote in the table
          create_qr = "insert into quotes_table(quote,author,category) values (%s,%s,%s)"
          values=(str(request.json["quote"]),str(request.json["author"]),str(request.json["category"]))
          try:
              #Executing insert query
              cursor.execute(create_qr,values)
              #Committing the results
              cnx.commit();
          except Exception as e:
              return '{"status":"Database Operation Failed","message":"'+str(e)+'"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
      except BaseException as be:
          return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
      finally:
          try:
             #Closing  db  connection
             cnx.close()
          except Exception as e:
             #Response returned if closing db connection fails
             return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
      #Success response returned on successful execution of request
      return '{"status":"success","message":"record created"}', 201, {'Content-Type': 'text/json; charset=utf-8'}
  else:
      #Response returned if user authentication fails
      return '{"status":"Authentication Failed","message":"Wrong Username or Password"}', 400, {
        'Content-Type': 'text/json; charset=utf-8'}

#POST method to delete quote record by quote_id
@app.route('/delete/', methods=['POST'])
def delete_a_quote():
    #Authentication check
    if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
        #returning bad request response if quote_id not in get request
        if request.json["quote_id"] is None or not request.json["quote_id"]:
            return '{"status":"Required Parameter Missing","message":""}', 400, {
                'Content-Type': 'text/json; charset=utf-8'}
        try:
            try:
                # Connect to the database
                cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                                  host='35.246.14.186',
                                                  database='QGram-db')
                cursor = cnx.cursor()
            except Exception as e:
                # response returned if connection to database fails
                return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                        'Content-Type': 'text/json; charset=utf-8'}
            #Delete query for  given quote_id
            delete_qr = "Delete from quotes_table where quote_id='"+request.json['quote_id']+"'"
            try:
                cursor.execute(delete_qr)
                #committing to db
                cnx.commit();
            except Exception as e:
                return '{"status":"Database Operation Failed","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
        except BaseException as be:
            return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        finally:
            try:
                cnx.close()
            except Exception as e:
                #response returned in case of db connection error
                return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
        #response returned on successful processing  of request
        return '{"status":"success","message":"record deleted"}', 200, {'Content-Type': 'text/json; charset=utf-8'}
    else:
        #Response returned if authentication fails
        return '{"status":"Authentication Failed","message":"Wrong Username or Password"}', 400, {
            'Content-Type': 'text/json; charset=utf-8'}

#GET method for getting quote by category
@app.route('/quote_by_category/<category>/', methods=['GET'])
def get_quote_by_category(category=''):
  category=category.strip()
  try:
    if category =='':
        return '{"status":"No Input Entered","message":""}', 400, {
            'Content-Type': 'text/json; charset=utf-8'}
    try:
            # Connect to the database
        cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                          host='35.246.14.186',
                                          database='QGram-db')
        cursor = cnx.cursor()
    except Exception as e:
        # response returned if connection fails to  db
        return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    #select query to get quotes from a particular category
    query = "SELECT * FROM quotes_table where category='"+category+"'"
    try:
        #execute select query
        cursor.execute(query)
    except Exception as e:
        #response returned if query fails
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    #response returned if no records present for given category
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
    #preparing output json
    records_json = "["
    #creating json for output
    for record in records:
        quote = str(record[1])
        #escaping double quotes
        quote = quote.replace('"', '&qt')
        records_json = records_json + '{"Quote_id":"' + str(
            record[0]) + '","Quote":"' + quote + '","Authors":"' + str(record[2]) + '","Category":"' + str(
            record[3]) + '"}'
        if record != records[-1]:
            records_json = records_json + ','
    records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
    try:
        #closing the connection
        cnx.close()
    except Exception as e:
        #exception response when database connection close fails
        return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  #output json
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

#GET method for getting quotes by quote_id
@app.route('/quote_by_quoteid/<quote_id>/', methods=['GET'])
def get_quote_by_quoteid(quote_id=''):
  quote_id=quote_id.strip()
  #returning error response if no quote_id recieved
  try:
    if quote_id =='':
        return '{"status":"No Input Entered","message":""}', 400, {
            'Content-Type': 'text/json; charset=utf-8'}
    try:
            # Connect to the database
        cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                          host='35.246.14.186',
                                          database='QGram-db')
        cursor = cnx.cursor()
    except Exception as e:
        #Response error if db connection failed
        return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    #select query for getting quotes by quote_id
    query = "SELECT * FROM quotes_table where quote_id='"+quote_id+"'"
    try:
        #execute query
        cursor.execute(query)
    except Exception as e:
        #Error response if select query fails
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    #Responding error if no records found with given quote_id
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
    #Building output json
    records_json = "["
        # records_str="<h1 align=\"center\">All Records</h1><table><tr><th>Quote Id</th><th>Quote</th><th>Author</th><th>Category</th></tr>"
    for record in records:
        quote = str(record[1])
        quote = quote.replace('"', '&qt')
        records_json = records_json + '{"Quote_id":"' + str(
            record[0]) + '","Quote":"' + quote + '","Authors":"' + str(record[2]) + '","Category":"' + str(
            record[3]) + '"}'
        if record != records[-1]:
            records_json = records_json + ','
    records_json = records_json + "]"
    # pprint("<h1>hello</h1>")
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
    try:
        #connection close
        cnx.close()
    except Exception as e:
        #Error if connection fails
        return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  #Response if success
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

#POST method to update records
@app.route('/update_quote_by_id/', methods=['POST'])
def update_quote_by_id():
  if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
      if request.json["quote_id"] is None or not request.json["quote_id"] and request.json["quote"] is None or not request.json["quote"]:
          return '{"status":"Required Parameter Missing","message":""}', 400, {
              'Content-Type': 'text/json; charset=utf-8'}
      try:
          try:
            #Connect to the database
               cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                          host='35.246.14.186',
                                          database='QGram-db')
               cursor = cnx.cursor()
          except Exception as e:
          #error response if connection fails to db
              return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
          try:
              #executing select query to find the quote with given quote_id
              cursor.execute("select * from quotes_table where quote_id="+request.json['quote_id'])
              records=cursor.fetchall()
              #response if no quote found with given quote id
              if len(records)==0:
                  return '{"status":"No Quote by quote id","message":""}', 404, {
                      'Content-Type': 'text/json; charset=utf-8'}
          except Exception as e:
              return '{"status":"Database Operation Failed","message":"'+str(e)+'"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
          #update query if author in get request
          if "author" in request.json:
              update_qr = "update quotes_table set quote='"+request.json['quote']+"', author='"+request.json['author']+"' where quote_id="+request.json['quote_id']
          #update query if author not in get request
          else:
              update_qr = "update quotes_table set quote='"+request.json['quote']+"' where quote_id="+request.json['quote_id']
          try:
              #execute update query
              cursor.execute(update_qr)
              #commit changes
              cnx.commit();
          except Exception as e:
              return '{"status":"Database Operation Failed","message":"'+str(e)+'"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
      except BaseException as be:
          return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
      finally:
          try:
             cnx.close()
          except Exception as e:
             return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
      #response if update successful
      return '{"status":"success","message":"record updated"}', 200, {'Content-Type': 'text/json; charset=utf-8'}
  else:
      #response if authentication fails
      return '{"status":"Authentication Failed","message":"Wrong Username or Password"}', 400, {
        'Content-Type': 'text/json; charset=utf-8'}

#GET API to translate a quote by quote id to a particular language. This api accepts quote_id and target language in request
@app.route('/update_quote_by_id/<id>/<t_lang>', methods=['GET'])
def translate(id,t_lang):
    try:
        try:
            # Connect to the database
            cnx = mysql.connector.connect(user='supervisor', password='supervisor351',
                                          host='35.246.14.186',
                                          database='QGram-db')
            cursor = cnx.cursor()
        except Exception as e:
            #Response error if connection to db fails
            return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        #query to get quote by quote id from the database
        query = "SELECT quote FROM quotes_table where quote_id="+id
        try:
            #Execute query
            cursor.execute(query)
        except Exception as e:
            return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        records = cursor.fetchall()
        #response if no records found with given quote_id
        if len(records) == 0:
            return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
        #Calling google translate api to get translation of the quote by given quote id into the given language
        response = requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+t_lang+"&dt=t&q='"+records[0][0]+"'")
        #parsing the response of the google translate api to json
        resp_json=response.json()
        #Creating output json to respond with the translation
        return str('{"Quote":"'+records[0][0]+'","language":"'+t_lang+'","translation":"'+resp_json[0][0][0]+'"}'), 200, {'Content-Type': 'text/json; charset=utf-8'}
    except BaseException as be:
        return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
    finally:
        try:
            #closing db connection
            cnx.close()
        except Exception as e:
            #Returning error response if connection to db fails
            return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
#Running flask app in main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)