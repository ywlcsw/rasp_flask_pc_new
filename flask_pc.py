from flask import Flask,render_template,redirect,request,url_for
from flask_bootstrap import Bootstrap
import time,json,os
import SQL,CRAWL_SQL_DATA,crawl_start

last_row_data_upload=[]
app = Flask(__name__)
bootstrap = Bootstrap(app)
redirect_to_chart_okFlag='not_ok'
SQL.init()
CRAWL_SQL_DATA.init()
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/redirect_to_home',methods=['GET','POST'])
def redirect_to_home():
    global redirect_to_chart_okFlag
    id1_id3_pure_data_list = crawl_start.get_spec_data()
    # time.sleep(1)
    if len(id1_id3_pure_data_list) == 40:
        # print(id1_id3_pure_data_list)
        # print(len(id1_id3_pure_data_list))
        crawl_start.add_to_sql(id1_id3_pure_data_list)
        crawl_start.id1_page = str(int(crawl_start.id1_page) + 1)
        crawl_start.id3_page = str(int(crawl_start.id3_page) + 1)
        crawl_start.id1_id3_pure_data_list = []
        # time.sleep(1)
        # print(id1_id3_pure_data_list)
    else:
        redirect_to_chart_okFlag = 'ok'
    # print(redirect_to_chart_okFlag,crawl_start.id1_page, crawl_start.id3_page)
    return redirect_to_chart_okFlag

@app.route('/redirect_to_home_page',methods=['GET','POST'])
def redirect_to_home_page():
    return crawl_start.id1_page

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    session = SQL.Session()
    rec_data = request.form
    if rec_data:
        json_data = json.dumps(rec_data)
        json_data_dict = json.loads(json_data)
        # print(json_data_dict)
        input_name=json_data_dict['username']
        input_pwd=json_data_dict['password']
        db_all_data=session.query(SQL.User).all()
        db_username_password_temporary=[]
        for all_row_obj in db_all_data:
            db_username_password_temporary.append(all_row_obj.username)
            db_username_password_temporary.append(all_row_obj.password)
            db_username_password_temporary.append(all_row_obj.realname)
        # print(db_username_password_temporary)
        if input_name not in db_username_password_temporary:
            return redirect((url_for('error_wrong_page')))
        if input_name in db_username_password_temporary:
            index=db_username_password_temporary.index(input_name)
            # print(index)
            if input_name==db_username_password_temporary[index] and input_pwd==db_username_password_temporary[index+1]:
                return redirect(url_for('logined',realname=db_username_password_temporary[index+2]))
            else:
                return redirect((url_for('error_wrong_page')))
    return render_template('login.html')

@app.route('/logined?realname=<realname>',methods=['GET','POST'])
def logined(realname):
    global last_row_data_upload
    session=CRAWL_SQL_DATA.Session()
    all_data=session.query(CRAWL_SQL_DATA.Crawl_data).all()
    last_row_data=all_data[-1]
    # print(last_row_data)
    last_row_data_upload=[last_row_data.date_time,last_row_data.co2,last_row_data.air_temp,last_row_data.air_humidity,last_row_data.illuminate,last_row_data.soil_temp,last_row_data.soil_humidity]
    # print(last_row_data_upload)
    session.close()
    return render_template('logined.html',realname=realname,last_row_data_upload=last_row_data_upload)

@app.route('/showtext',methods=['GET','POST'])
def showtext():
    session=SQL.Session()
    str_content=session.query(SQL.Content).filter(SQL.Content.id==1).first().text
    session.close()
    # print(str_content)
    return json.dumps(str_content)

@app.route('/savetext',methods=['GET','POST'])
def savetext():
    session=SQL.Session()
    text_contents=request.args.get('text_save')
    # print(text_contents)
    session.query(SQL.Content).filter(SQL.Content.id==1).update({'text':text_contents})
    session.commit()
    session.close()
    return json.dumps('ok')

@app.route('/refresh?realname=<realname>',methods=['GET','POST'])
def refresh(realname):
    # time.sleep(1)
    global last_row_data_upload
    while True:
        id1_id3_pure_data_list = crawl_start.get_spec_data()
        if len(id1_id3_pure_data_list)==40:
            # print(id1_id3_pure_data_list)
            # print(len(id1_id3_pure_data_list))
            crawl_start.add_to_sql(id1_id3_pure_data_list)
            crawl_start.id1_page = str(int(crawl_start.id1_page) + 1)
            crawl_start.id3_page = str(int(crawl_start.id3_page) + 1)
            crawl_start.id1_id3_pure_data_list = []
            # print(id1_id3_pure_data_list)
            session = CRAWL_SQL_DATA.Session()
            all_data = session.query(CRAWL_SQL_DATA.Crawl_data).all()
            last_row_data = all_data[-1]
            # print(last_row_data)
            last_row_data_upload = [last_row_data.date_time, last_row_data.co2, last_row_data.air_temp,
                                    last_row_data.air_humidity, last_row_data.illuminate, last_row_data.soil_temp,
                                    last_row_data.soil_humidity]
            # print(last_row_data_upload)
            session.close()
        else:
            break
    # print(crawl_start.id1_page,crawl_start.id3_page)
    return render_template('logined.html',realname=realname,last_row_data_upload=last_row_data_upload)

@app.route('/chart?realname=<realname>',methods=['GET','POST'])
def chart(realname):
    session=CRAWL_SQL_DATA.Session()
    all_data=session.query(CRAWL_SQL_DATA.Crawl_data).all()
    all_data_list= []
    all_data_list_upload=[]
    for data in all_data:
        all_data_list.append(data.date_time)
        all_data_list.append(data.co2)
        all_data_list.append(data.air_temp)
        all_data_list.append(data.air_humidity)
        if ',' in data.illuminate:
            illuminate_digit=filter(str.isdigit, data.illuminate)
            illuminate_digits=''.join(list(illuminate_digit))
            all_data_list.append(illuminate_digits)
        else:
            all_data_list.append(data.illuminate)
        all_data_list.append(data.soil_temp)
        all_data_list.append(data.soil_humidity)
        all_data_list_upload.append(all_data_list)
        all_data_list=[]
    # print(all_data_list_upload)
    session.close()
    return render_template('chart.html',realname=realname,all_data_list_upload=all_data_list_upload)

@app.route('/graph?realname=<realname>',methods=['GET','POST'])
def graph(realname):
    session=CRAWL_SQL_DATA.Session()
    all_data=session.query(CRAWL_SQL_DATA.Crawl_data).all()
    all_data_list= []
    all_data_list_upload=[]
    for data in all_data:
        all_data_list.append(data.date_time)
        all_data_list.append(data.co2)
        all_data_list.append(data.air_temp)
        all_data_list.append(data.air_humidity)
        if ',' in data.illuminate:
            illuminate_digit=filter(str.isdigit, data.illuminate)
            illuminate_digits=''.join(list(illuminate_digit))
            all_data_list.append(illuminate_digits)
        else:
            all_data_list.append(data.illuminate)
        all_data_list.append(data.soil_temp)
        all_data_list.append(data.soil_humidity)
        all_data_list_upload.append(all_data_list)
        all_data_list=[]
    # print(all_data_list_upload)
    session.close()
    return render_template('graph.html',realname=realname,all_data_list_upload=all_data_list_upload)

@app.route('/registration/',methods=['GET','POST'])
def registration():
    session = SQL.Session()
    # print('请求头:%s' % request.headers)  # 打印结果为请求头信息
    # print('请求方式:%s' % request.method)  # GET
    # print('请求url地址:%s' % request.url)
    rec_data = request.form
    json_data = json.dumps(rec_data)
    json_data_dict = json.loads(json_data)
    # print(json_data_dict)
    if json_data_dict:
        username = json_data_dict['form-user_name']
        realname = json_data_dict['form-real_name']
        password = json_data_dict['form-password']
        email = json_data_dict['form-email']
        if realname and realname and password and email:
            db_all_data = session.query(SQL.User).all()
            db_username_temporary = []
            for all_row_obj in db_all_data:
                db_username_temporary.append(all_row_obj.username)
            if username in db_username_temporary:
                return redirect(url_for('error_replicate_name'))
            else:
                user_to_db=SQL.User(username=username,realname=realname,password=password,email=email)
                session.add(user_to_db)
                session.commit()
                session.close()
                return redirect(url_for('login'))
            # print(json_data_dict)
    return render_template('registration.html')

@app.route('/error_replicate_name/')
def error_replicate_name():
    return render_template('error_replicate_name.html')

@app.route('/error_wrong_page/')
def error_wrong_page():
    return render_template('error_wrong_page.html')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=8787,debug=True)
