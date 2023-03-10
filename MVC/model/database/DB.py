import os
import psycopg2
import sqlite3
from supabase import create_client

SUPABASE_URL = "https://euvyjxtkzixoflcdcwof.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImV1dnlqeHRreml4b2ZsY2Rjd29mIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY3NTg5OTU0OCwiZXhwIjoxOTkxNDc1NTQ4fQ.a_VUtdmAJcIfZi4WLLS8jdK5nQiHqKOXCTsy5YBPSq8"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

#data = supabase.table("Team22Lasertag").select("*").execute()
#data = supabase.table("Team22Lasertag").insert({"code": "Beast", "firstname": "Trey", "lastname": "Hurlbut", "playerid": 2342}).execute()


class Database():
    DB_NO_CONN = 0
    DB_SUPABASE = 1
    DB_SQLITE = 2

    def __init__(self):
        print("Connecting to Database...")
        self.conn = None
        self.cursor = None
        self.intConnection = Database.DB_NO_CONN
        self.strSelectedTable = "player"


    def selectTable(self, strTableName):
        self.strSelectedTable = strTableName

    def getAllTables(self):
        if self.cursor is not None:
            self.cursor.execute("""
            SELECT * FROM information_schema.tables WHERE table_schema='public';""")
            return self.cursor.fetchall()
        else:
            return []

    def getAllRows(self):
        try:
            if self.cursor is not None:
                self.cursor.execute("SELECT * FROM {table} ORDER BY id".format(table=self.strSelectedTable))
                rows = self.cursor.fetchall()
                return rows
            else:
                return []
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error:")
            print(error)
            return None

    def deleteById(self, id):
        try:
            if self.cursor is not None:
                data = [id]
                if self.intConnection == Database.DB_SUPABASE:
                    self.cursor.execute(
                        "DELETE FROM {table} WHERE id=%s RETURNING *".format(table=self.strSelectedTable), data)
                    rows = self.cursor.fetchall()
                    return rows
                else:
                    self.cursor.execute(
                        "DELETE FROM {table} WHERE id=? RETURNING *".format(table=self.strSelectedTable), data)
                    rows = self.cursor.fetchall()
                    return rows
            else:
                return []
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error:")
            print(error)
            return None

    def getLastId(self):
        try:
            if self.cursor is not None:
                self.cursor.execute("""
                SELECT id, first_name, last_name, codename 
                FROM {table} ORDER BY id DESC LIMIT 1""".format(table=self.strSelectedTable));
                rows = self.cursor.fetchall()
                return rows
            else:
                return []
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error:")
            print(error)
            return None

    def findId(self, id):
        if self.cursor is not None:
            data = [id]
            if self.intConnection == Database.DB_SUPABASE:
                self.cursor.execute("""
                SELECT * FROM {table} WHERE id=%s;""".format(table=self.strSelectedTable), data)
                return self.cursor.fetchall()
            else:
                self.cursor.execute("""
                SELECT * FROM {table} WHERE id=?;""".format(table=self.strSelectedTable), data)
                return self.cursor.fetchall()
        else:
            return []

    def updateUsingId(self, listPlayerInfo):
        if self.isPlayerInfoValid(listPlayerInfo):
            if self.cursor is not None:
                data = [listPlayerInfo[1], listPlayerInfo[2], listPlayerInfo[3], listPlayerInfo[0]]
                if self.intConnection == Database.DB_SUPABASE:
                    self.cursor.execute("""
                    UPDATE {table} 
                    SET first_name=%s, last_name=%s, codename=%s WHERE id=%s;
                    """.format(table=self.strSelectedTable), data)
                else:
                    self.cursor.execute("""
                    UPDATE {table} 
                    SET first_name=?, last_name=?, codename=? WHERE id=?;
                    """.format(table=self.strSelectedTable), data)
            else:
                pass
        else:
            print("Error: listPlayerInfo is incorrect size. Cannot add to DB")

    def insertPlayer(self, listPlayerInfo):
        supabase.table("Team22Lasertag").insert({"code": listPlayerInfo[3],
                                                 "firstname": listPlayerInfo[1],
                                                 "lastname": listPlayerInfo[2],
                                                 "playerid": listPlayerInfo[0]}).execute()

    def deleteAllRows(self):
        supabase.table("Team22Lasertag").delete().gte("playerid", -1).execute()

    def isPlayerInfoValid(self, listPlayerInfo):
        isListSizeValid = len(listPlayerInfo) == 4
        if isListSizeValid:
            isTypeValid = type(listPlayerInfo[0]) is int and type(listPlayerInfo[1]) is str and type(
                listPlayerInfo[2]) is str and type(listPlayerInfo[3]) is str
            if isTypeValid:
                isStrSizeValid = len(listPlayerInfo[1]) <= 30 and len(listPlayerInfo[2]) <= 30 and len(
                    listPlayerInfo[3]) <= 30
                return isStrSizeValid
            return False
        return False

    def findPlayerByName(self, firstName, lastName):
        if self.cursor is not None:
            data = (firstName.upper(), lastName.upper())
            if self.intConnection == Database.DB_SUPABASE:
                self.cursor.execute("""
                SELECT person.id, person.first_name, person.last_name, person.codename
                FROM {table} AS person
                    INNER JOIN {table} AS returnValue
                    ON UPPER(person.first_name) = %s
                    AND UPPER(person.last_name) = %s
                GROUP BY person.id, person.first_name, person.last_name, person.codename
                ORDER BY person.id, person.first_name, person.last_name, person.codename""".format(
                    table=self.strSelectedTable), data)
                return self.cursor.fetchall()
            else:
                self.cursor.execute("""
                SELECT person.id, person.first_name, person.last_name, person.codename
                FROM {table} AS person
                    INNER JOIN {table} AS returnValue
                    ON UPPER(person.first_name) = ?
                    AND UPPER(person.last_name) = ?
                GROUP BY person.id, person.first_name, person.last_name, person.codename
                ORDER BY person.id, person.first_name, person.last_name, person.codename""".format(
                    table=self.strSelectedTable), data)
                return self.cursor.fetchall()
        else:
            return []



    def commit(self):
        if self.conn is not None:
            self.conn.commit()

    def closeDB_NoCommit(self):
        if self.conn is not None:
            self.cursor.close()
            self.conn.close()

    def closeDB_Commit(self):
        if self.conn is not None:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
