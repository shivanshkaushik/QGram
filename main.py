#Importing the necessary libraries
import mysql.connector
from flask import Flask, request
import requests


app = Flask(__name__)

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
        #raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Error","message":"'+str(e)+'"}', 500, {'Content-Type': 'text/json; charset=utf-8'}
        #if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
    query = "SELECT * FROM quotes_table"
    try:
        cursor.execute(query)
    except Exception as e:
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    if len(records)==0:
        return '{"status":"No Records Found","message":""}', 404, {
            'Content-Type': 'text/json; charset=utf-8'}
    records_json="["
    #records_str="<h1 align=\"center\">All Records</h1><table><tr><th>Quote Id</th><th>Quote</th><th>Author</th><th>Category</th></tr>"
    for record in records:
        quote=str(record[1])
        quote=quote.replace('"','&qt')
        records_json=records_json+'{"Quote_id":"'+str(record[0])+'","Quote":"'+quote+'","Authors":"'+str(record[2])+'","Category":"'+str(record[3])+'"}'
        if record!=records[-1]:
            records_json=records_json+','
        #records_str=records_str+"<tr><td>"+str(record[0])+"</td><td>"+str(record[1])+"</td><td>"+str(record[3])+"</td><td>"+str(record[2])+"</td></tr>"
    records_json = records_json + "]"
           #pprint("<h1>hello</h1>")
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
          'Content-Type': 'text/json; charset=utf-8'}
  finally:
        try:
            cnx.close()
        except Exception as e:
            # raise ConnectionError('Cannot connect to database')
            return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

        #return make_response('Could not verify!', 401,{'WWW-Authenticate':'Basic realm="Login Required"'})

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
        #raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Error","message":"'+str(e)+'"}', 500, {'Content-Type': 'text/json; charset=utf-8'}
    query="select author from quotes_table";
    try:
        cursor.execute(query)
    except exception as e:
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
            'Content-Type': 'text/json; charset=utf-8'}
    #records_str="<h1 align=\"center\">All Authors</h1><table><tr><th>Authors</th></tr>"
    records_json=''
    for record in records:
        records_json = records_json + '{"Author":"' + str(record[0]) + '"}'
        if record != records[-1]:
            records_json = records_json + ','
        # records_str=records_str+"<tr><td>"+str(record[0])+"</td><td>"+str(record[1])+"</td><td>"+str(record[3])+"</td><td>"+str(record[2])+"</td></tr>"
    records_json = records_json + "]"
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
      try:
          cnx.close()
      except Exception as e:
          # raise ConnectionError('Cannot connect to database')
          return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

@app.route('/quote_by_authors/<author_name>/', methods=['GET'])
def get_quote_by_author(author_name=''):
  try:
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
        # raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        # if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
    query = "SELECT * FROM quotes_table where author='"+author_name+"'"
    try:
        cursor.execute(query)
    except Exception as e:
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
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
        # records_str=records_str+"<tr><td>"+str(record[0])+"</td><td>"+str(record[1])+"</td><td>"+str(record[3])+"</td><td>"+str(record[2])+"</td></tr>"
    records_json = records_json + "]"
    # pprint("<h1>hello</h1>")
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
    try:
        cnx.close()
    except Exception as e:
        # raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

@app.route('/create/', methods=['POST'])
def create_a_quote():
  if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
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
          # raise ConnectionError('Cannot connect to database')
              return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
          create_qr = "insert into quotes_table(quote,author,category) values (%s,%s,%s)"
          values=(str(request.json["quote"]),str(request.json["author"]),str(request.json["category"]))
          try:
              cursor.execute(create_qr,values)
              cnx.commit();
          except Exception as e:
              return '{"status":"Database Operation Failed","message":"'+str(e)+'"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        #all_records.append(new_record)
      except BaseException as be:
          return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
      finally:
          try:
             cnx.close()
          except Exception as e:
             # raise ConnectionError('Cannot connect to database')
             return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
      return '{"status":"success","message":"record created"}', 201, {'Content-Type': 'text/json; charset=utf-8'}
  else:
      return '{"status":"Authentication Failed","message":"Wrong Username or Password"}', 400, {
        'Content-Type': 'text/json; charset=utf-8'}

@app.route('/delete/', methods=['POST'])
def delete_a_quote():
    if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
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
                # raise ConnectionError('Cannot connect to database')
                return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                        'Content-Type': 'text/json; charset=utf-8'}
            delete_qr = "Delete from quotes_table where quote_id='"+request.json['quote_id']+"'"
            try:
                cursor.execute(delete_qr)
                cnx.commit();
            except Exception as e:
                return '{"status":"Database Operation Failed","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
        # all_records.append(new_record)
        except BaseException as be:
            return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        finally:
            try:
                cnx.close()
            except Exception as e:
                # raise ConnectionError('Cannot connect to database')
                return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
        return '{"status":"success","message":"record deleted"}', 200, {'Content-Type': 'text/json; charset=utf-8'}
    else:
        return '{"status":"Authentication Failed","message":"Wrong Username or Password"}', 400, {
            'Content-Type': 'text/json; charset=utf-8'}

@app.route('/quote_by_category/<category>/', methods=['GET'])
def get_quote_by_category(category=''):
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
        # raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        # if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
    query = "SELECT * FROM quotes_table where category='"+category+"'"
    try:
        cursor.execute(query)
    except Exception as e:
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
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
        # records_str=records_str+"<tr><td>"+str(record[0])+"</td><td>"+str(record[1])+"</td><td>"+str(record[3])+"</td><td>"+str(record[2])+"</td></tr>"
    records_json = records_json + "]"
    # pprint("<h1>hello</h1>")
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
    try:
        cnx.close()
    except Exception as e:
        # raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

@app.route('/quote_by_quoteid/<quote_id>/', methods=['GET'])
def get_quote_by_quoteid(quote_id=''):
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
        # raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        # if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
    query = "SELECT * FROM quotes_table where quote_id='"+quote_id+"'"
    try:
        cursor.execute(query)
    except Exception as e:
        return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
    records = cursor.fetchall()
    if len(records) == 0:
        return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
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
        # records_str=records_str+"<tr><td>"+str(record[0])+"</td><td>"+str(record[1])+"</td><td>"+str(record[3])+"</td><td>"+str(record[2])+"</td></tr>"
    records_json = records_json + "]"
    # pprint("<h1>hello</h1>")
  except BaseException as be:
    return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
        'Content-Type': 'text/json; charset=utf-8'}
  finally:
    try:
        cnx.close()
    except Exception as e:
        # raise ConnectionError('Cannot connect to database')
        return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
              'Content-Type': 'text/json; charset=utf-8'}
  return records_json, 200, {'Content-Type': 'text/json; charset=utf-8'}

@app.route('/update_quote_by_id/', methods=['POST'])
def update_quote_by_id():
  if request.json['username']=='supervisor' and request.json['password']=='supervisor351':
      if request.json["quote_id"] is None or not request.json["quote_id"] and request.json["quote"] is None or not request.json["quote"]:
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
          # raise ConnectionError('Cannot connect to database')
              return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                    'Content-Type': 'text/json; charset=utf-8'}
          try:
              cursor.execute("select * from quotes_table where quote_id="+request.json['quote_id'])
              records=cursor.fetchall()
              if len(records)==0:
                  return '{"status":"No Quote by quote id","message":""}', 404, {
                      'Content-Type': 'text/json; charset=utf-8'}
          except Exception as e:
              return '{"status":"Database Operation Failed","message":"'+str(e)+'"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
          if "author" in request.json:
              update_qr = "update quotes_table set quote='"+request.json['quote']+"', author='"+request.json['author']+"' where quote_id="+request.json['quote_id']
          else:
              update_qr = "update quotes_table set quote='"+request.json['quote']+"' where quote_id="+request.json['quote_id']
          try:
              cursor.execute(update_qr)
              cnx.commit();
          except Exception as e:
              return '{"status":"Database Operation Failed","message":"'+str(e)+'"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        #all_records.append(new_record)
      except BaseException as be:
          return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
      finally:
          try:
             cnx.close()
          except Exception as e:
             # raise ConnectionError('Cannot connect to database')
             return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
      return '{"status":"success","message":"record updated"}', 200, {'Content-Type': 'text/json; charset=utf-8'}
  else:
      return '{"status":"Authentication Failed","message":"Wrong Username or Password"}', 400, {
        'Content-Type': 'text/json; charset=utf-8'}

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
            # raise ConnectionError('Cannot connect to database')
            return '{"status":"Database Connection Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
            # if request.authorization and request.authorization.username == 'username' and request.authorization.password == 'password':
        query = "SELECT quote FROM quotes_table where quote_id="+id
        try:
            cursor.execute(query)
        except Exception as e:
            return '{"status":"Data Fetch Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}
        records = cursor.fetchall()
        if len(records) == 0:
            return '{"status":"No Records Found","message":""}', 404, {
                'Content-Type': 'text/json; charset=utf-8'}
        response = requests.get("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl="+t_lang+"&dt=t&q='"+records[0][0]+"'")
        resp_json=response.json()
        return str('{"Quote":"'+records[0][0]+'","language":"'+t_lang+'","translation":"'+resp_json[0][0][0]+'"}'), 200, {'Content-Type': 'text/json; charset=utf-8'}
    except BaseException as be:
        return '{"status":"Some Error Occured","message":"' + str(be) + '"}', 500, {
            'Content-Type': 'text/json; charset=utf-8'}
    finally:
        try:
            cnx.close()
        except Exception as e:
            return '{"status":"Database Connection Close Error","message":"' + str(e) + '"}', 500, {
                'Content-Type': 'text/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)