from digi.xbee.devices import XBeeDevice
from digi.xbee.devices import RemoteXBeeDevice
from digi.xbee.devices import XBee64BitAddress
import psycopg2
PORT = "COM9"
conn = psycopg2.connect(
        database="postgres", user='postgres', password='password', host='127.0.0.1', port='5432'
    )
conn.autocommit = True

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

# Creating a database
cursor.execute("CREATE TABLE data(id SERIAL_PRIMARY_KEY ,name Raw, name Read)")
conn.commit()
print("Database created successfully........")

# Closing the connection
conn.close()
class RadioDriver():
    device = XBeeDevice("COM9", 9600)
    device.open()

    # Closing the connection
    conn.close()
    def radio_read(self):
        ##read from digi
        message = self.device.add_data_received_callback(self.data_receive_callback)
        ##write to database
        cursor.execute("INSERT INTO data (id) VALUE(%s)",SERIAL_PRIMARY_KEY)

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

