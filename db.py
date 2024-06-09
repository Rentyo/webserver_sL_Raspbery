import pymysql
import socket
import base64
from PIL import Image
import io
def dbConnect(msg, data=''):
    conn = pymysql.connect(host='IP', 
                        user='user',
                        password='password',
                        charset='utf8',
                        db = 'dbname') 
    cursor = conn.cursor() 
    ip_address = extract_ip()
    #GPS DB
    if(msg == 'gps'):
        sql = """
        UPDATE device
        SET latitude = %s, longitude = %s
        WHERE device_ip_address = %s
        """
        
        data_to_update = (data['lati'], data['long'], ip_address)

        try:
            
            cursor.execute(sql, data_to_update)
            
            conn.commit()
            print("업데이트 성공")
        except pymysql.Error as err:
            print("업데이트 실패: {}".format(err))
            
            conn.rollback()
        finally:
            # 커서와 연결 종료
            cursor.close()
            conn.close()
    #온습도 DB
    elif(msg == 'tem_hum'):
        sql1 = """
        Select device_num, location 
        From device 
        WHERE device_ip_address = %s
        """

        data_to_update = (ip_address)
        datas = ""
        try:
            cursor.execute(sql1, data_to_update)
            datas = cursor.fetchall()
            print(datas[0][0]) 
        except pymysql.Error as err:
            print("업데이트 실패: {}".format(err))
            
            conn.rollback()
        print(datas)
        daynight = 0
        if (data['time'].hour >=12):
            daynight = 1
        sql2 = """
        INSERT INTO device_data (device_num, temp, humi, `current_date`, day_night, `current_time`, location) 
        VALUE (%s ,%s ,%s ,%s ,%s ,%s, %s)
        """

        data_to_update = (datas[0][0] , data['temp'][0], data['hum'], data['date'], daynight, data['time'], datas[0][1])
        try:    
            cursor.execute(sql2, data_to_update)  
               
            conn.commit()
            print("삽입 성공")
        except pymysql.Error as err:
            print("삽입 실패: {}".format(err))
            
            conn.rollback()
        finally:
            # 커서와 연결 종료
            cursor.close()
            conn.close()
    #진동 db
    elif(msg == 'crash'):
        sql1 = """
        Select device_num 
        From device 
        WHERE device_ip_address = %s
        """

        data_to_update = (ip_address)
        datas = ""
        try:
            cursor.execute(sql1, data_to_update)
            datas = cursor.fetchall()
            print(datas[0][0]) 
        except pymysql.Error as err:
            print("업데이트 실패: {}".format(err))
            
            conn.rollback()
        sql2 = """
        INSERT INTO error (device_num, `current_time`, error_content, crash, current_image) 
        VALUE (%s ,%s ,%s ,%s ,%s)
        """
 
        data_to_update = (datas[0][0] , data['time'], str(data['time']) +'경 충돌이 발생했습니다', 1, data['image'])
        try:    
            cursor.execute(sql2, data_to_update)      
            conn.commit()
            print("삽입 성공")
        except pymysql.Error as err:
            print("삽입 실패: {}".format(err))
            
            conn.rollback()
        finally:
            # 커서와 연결 종료
            cursor.close()
            conn.close()
#DEVICE IP 추출
def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(("10.255.255.255", 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        st.close()
    return IP
