from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import psycopg2
PORT = "COM9"
class RadioDriver():
    device = XBeeDevice(PORT, 9600)
    device.open()
    global PORT
    def radio_read(self):
        ##read from digi
        message = self.device.add_data_received_callback(self.data_receive_callback)
        ##write to database
        try:
            connection = psycopg2.connect(user="sysadmin",
                                      password="pynative@#29",
                                      host="127.0.0.1",
                                      port="9600",
                                      database="postgres_db")
            cursor = connection.cursor()
            postgres_insert_query = """ INSERT (ID, Text, READ) VALUES (%s,%s,%b)"""
            record_to_insert = (PRIMARY_KEY, message, True);
            cursor.execute(postgres_insert_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into mobile table")
        except (Exception, psycopg2.Error) as error:
            print("Failed to insert record into table: ", error)
        ##PRIMARY_KEY AUTO_INCREMENT;
        return 0
    def radio_send(self):
        ##read from database
        ##send to database
        return 0
    def data_receive_callback(xbee_message):
        packet = xbee_message.data.decode()
        return packet
        ##self.logger.info("Packet received ~~~~~~")
        ##self.logger.info(packet)

    ##CREATE TABLE data(
      ##  id  SERIAL PRIMARY KEY;
   ## );

