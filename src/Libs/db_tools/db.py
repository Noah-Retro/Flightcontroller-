import sqlite3
import threading
import datetime
import pandas as pd
import numpy as np
import json

def generate_smooth_random_walk(num_samples, std_dev=0.05):
    data = {'Timestamp': pd.date_range(start='2024-01-06', periods=num_samples, freq='S')}
    columns = ['Timestamp', 'Acceleration_X', 'Acceleration_Y', 'Acceleration_Z', 'Gyro_X', 'Gyro_Y', 'Gyro_Z']

    for col in columns[1:]:
        data[col] = np.cumsum(np.random.normal(0, std_dev, num_samples))

    return pd.DataFrame(data)
    


class DbHandler():
    def __init__(self,path:str="Flightcontroller-/src/DB/flight_data.db",schema_path:str="Flightcontroller-/src/Libs/db_tools/schema.sql") -> None:
        self.path = path
        self.con = sqlite3.connect(self.path)
        self.cur = self.con.cursor()
        self.schema_path = schema_path

        with open(self.schema_path,encoding="utf8") as f:
            self.con.executescript(f.read())

    def delDb(self)->None:
        """Deletes all tables from the DB.
        The data will be lost without a recovery possibility
        """
        self.cur.execute("Drop table mpu;")
        self.con.commit()

    def storeMPUData(self,df:pd.DataFrame)->None:
        """stores all MPU data with timestamp of reading

        Args:
            mpu (MPU9250): The connected MPU
        """

        data = open("Flightcontroller-\src\settings\data.json")
        settings = json.load(data)
        data.close()
        flight_num = settings["fligth_num"]

        for _ in df["Timestamp"]:
            df["FlightNum"] = flight_num

        df.to_sql('mpu', con=self.con,
                  schema=open(self.schema_path,encoding="utf8").read(),
                   if_exists='replace',
                     index=False)
        self.con.commit()


    def storeTestData(self,numEntry:int,std_dev:float=0.05)->None:
        """Populates the db with Pandas test data

        Args:
            numEntry (int): How many entrys will be created
        """
        df = generate_smooth_random_walk(numEntry,std_dev=std_dev)
        data = open("Flightcontroller-\src\settings\data.json")
        settings = json.load(data)
        data.close()
        flight_num = settings["fligth_num"]

        for _ in df["Timestamp"]:
            df["FlightNum"] = flight_num

        df.to_sql('mpu', con=self.con,
                  schema=open(self.schema_path,encoding="utf8").read(),
                   if_exists='replace',
                     index=False)
        self.con.commit()

    def load_test_data(self):
        # Query to select all columns from the mpu table
        query = 'SELECT * FROM mpu;'

        # Read the data into a Pandas DataFrame
        df = pd.read_sql_query(query, self.con)

        return df
            


if __name__ == "__main__":

    db = DbHandler()
    db.storeTestData(100)
    print(db.load_test_data())

