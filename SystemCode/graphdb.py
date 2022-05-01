#from cProfile import label
from re import S
from unittest import result
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
#from py2neo import Graph
import sys
import string



class Recommender:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def close(self):
        self.driver.close()
    
    def clearDB(self):
        query = "match (n) detach delete (n)"
        with self.driver.session() as graphDB_Session:
            rcv = graphDB_Session.run(query)
            print(rcv)

    def createDB(self):
        query = '''CREATE (tm:Robot {name:"TM"})-[:HAS_GRIPPER]->(g1:Gripper {name:"g1"}),
                (tm)-[:HAS_GRIPPER]->(g2:Gripper {name:"g2"}),
                (tm)-[:HAS_GRIPPER]->(g3:Gripper {name:"g3"}),
                (tm)-[:HAS_GRIPPER]->(g4:Gripper {name:"g4"}),
                (red:Color {name:"RED"}),
                (blue:Color {name:"BLUE"}),
                (green:Color {name:"GREEN"}),
                (black:Color {name:"BLACK"}),
                (orange:Color {name:"ORANGE"}),
                (circle:Shape {name:"CIRCLE"}),
                (p41:Position {name:"P41"}),
                (p42:Position {name:"P42"}),
                (p43:Position {name:"P43"}),
                (p44:Position {name:"P44"}),
                (p45:Position {name:"P45"}),
                (p46:Position {name:"P46"}),
                (p01:Position {name:"P01"}),
                (p02:Position {name:"P02"}),

                (casing:Itemname {name:"CASING"})-[:COLOR]->(black),
                (casing)-[:SHAPE]->(rectangle:Shape {name:"RECTANGLE"}),
                (casing)-[:POSITION]->(p01),
                (g1)-[:PICKS]->(casing),
                (filler:Itemname {name:"FILLER"})-[:COLOR]->(black),
                (filler)-[:SHAPE]->(rectangle),
                (filler)-[:POSITION]->(p02),
                (g1)-[:PICKS]->(filler),

                (redcoins:Itemname {name:"REDCOINS"})-[:COLOR]->(red),(redcoins)-[:POSITION]->(p41),
                (redcoins)-[:SHAPE]->(circle),
                (redcoins)-[:POSITION]->(p42),
                (redcoins)-[:POSITION]->(p43),
                (g2)-[:PICKS]->(redcoins),

                (greencoins:Itemname {name:"GREENCOINS"})-[:COLOR]->(green),(greencoins)-[:POSITION]->(p44),
                (greencoins)-[:SHAPE]->(circle),
                (greencoins)-[:POSITION]->(p45),
                (greencoins)-[:POSITION]->(p46),
                (g2)-[:PICKS]->(greencoins),


                (bluecoins:Itemname {name:"BLUECOINS"})-[:COLOR]->(blue),(bluecoins)-[:POSITION]->(p43),
                (bluecoins)-[:SHAPE]->(circle),
                (bluecoins)-[:POSITION]->(p46),
                (g2)-[:PICKS]->(bluecoins),

                (orangecoins:Itemname {name:"ORANGECOINS"})-[:COLOR]->(orange),(orangecoins)-[:POSITION]->(p42),
                (orangecoins)-[:SHAPE]->(circle),
                (orangecoins)-[:POSITION]->(p45),
                (g2)-[:PICKS]->(orangecoins)'''

        with self.driver.session() as graphDB_Session:
            rcv = graphDB_Session.run(query)
            print(rcv) 

    def querygripper(self):
        query = '''WITH ['g2'] as names
                   MATCH (g:Gripper)-[:PICKS]->(i:Itemname) WHERE g.name in names 
                   RETURN DISTINCT i.name As iname'''
        with self.driver.session() as graphDB_Session:
            result  = graphDB_Session.run(query)
            result  = ([record["iname"] for record in result])
            #print(*result)
            return result

    def queryplaceforcolor(self,value):
        s = '"'+value.upper()+'"'
        query = '''MATCH (Position)<-[:POSITION]-(color)-[:COLOR]->('''+value+''':Color {name: '''+s+'''})
                   RETURN DISTINCT Position.name As pname'''
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(query)
            result  = ([record["pname"] for record in result])
            print("position for color:", result[0])
            return result[0]

    def querygripperwidth(self,value):
        CL = '"'+value.upper()+'"'
        query = '''MATCH (Gwidth)<-[:GWIDTH]-(color)-[:COLOR]->('''+value+''':Color {name: '''+CL+'''})
                   RETURN DISTINCT Gwidth.name As pname'''
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(query)
            result  = ([record["pname"] for record in result])
            print("Gripper width is :", result[0])
            return "w_30"
    
    def queryangle(self,value):
        CL = '"'+value.upper()+'"'
        query = '''MATCH (Elbow)<-[:J3ANGLE]-(color)-[:COLOR]->('''+value+''':Color {name: '''+CL+'''})
                   RETURN DISTINCT Elbow.name As pname'''
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(query)
            result  = ([record["pname"] for record in result])
            print("Joint3 angle :", result[0])
            return result[0]

    def queryplaceposition(self):
        query = '''MATCH (Position)<-[:POSITION]-(color)-[:COLOR]->(red:Color {name: "RED"})
                   MATCH (Position)<-[:POSITION]-(shape)-[:SHAPE]->(circle:Shape {name: "CIRCLE"})
                   RETURN DISTINCT Position.name As pname'''
        with self.driver.session() as graphDB_Session:
            result = graphDB_Session.run(query)
            result  = ([record["pname"] for record in result])
            print(*result)
            return result

    def querypickattrib(self, pos):
        t = pos.upper()
        #{name: $person_name}
        #print(pos,'/n',t)
        s = "("+pos+''':Position {name: "'''+t+'''"})'''
        query = '''MATCH (c:Color)<-[:COLOR]-(color)-[:POSITION]->'''+s+'''
                   MATCH (s:Shape)<-[:SHAPE]-(shape)-[:POSITION]->'''+s+'''
                   RETURN DISTINCT c.name AS colorname,s.name AS shapename'''
    
        with self.driver.session() as graphDB_Session:
            result  = graphDB_Session.run(query)
            #return [{"restaurant": row["name"], "likers": row["likers"], "occurence": row["occurence"]} for row in result]
            result  = [{"colorname":row["colorname"], "shapename":row["shapename"]} for row in result]
            print(*result)
            #for r in result :
            #    print(r)
            return result

    def update(self,iname,gwidth,eangle,finalxy,ctime,dist):
        GW = gwidth.upper()
        EA = eangle.upper()
        IN = iname.upper()
        FXY = finalxy.upper()
        CT = ctime.upper()
        DIST = dist.upper()
        
        query = '''CREATE('''+gwidth+''':Gwidth {name:"'''+GW+'''"})
                    CREATE('''+eangle+''':Elbow {name:"'''+EA+'''"})
                    CREATE('''+finalxy+''':Finalxy {name:"'''+FXY+'''"})
                    CREATE('''+ctime+''':Ctime {name:"'''+CT+'''"})
                    CREATE('''+dist+''':Distance {name:"'''+DIST+'''"})'''

        query1= '''    MATCH('''+gwidth+''':Gwidth {name:"'''+GW+'''"})
            MATCH('''+eangle+''':Elbow {name:"'''+EA+'''"})
            MATCH('''+finalxy+''':Finalxy {name:"'''+FXY+'''"})
            MATCH('''+ctime+''':Ctime {name:"'''+CT+'''"})
            MATCH('''+dist+''':Distance {name:"'''+DIST+'''"})
            MATCH('''+iname+''':Itemname {name:"'''+IN+'''"})
            CREATE('''+iname+''')-[:GWIDTH]->('''+gwidth+''')
            CREATE('''+iname+''')-[:J3ANGLE]->('''+eangle+''')
            CREATE('''+iname+''')-[:FINALXY]->('''+finalxy+''')
            CREATE('''+iname+''')-[:CTIME]->('''+ctime+''')
            CREATE('''+iname+''')-[:DISTANCE]->('''+dist+''')'''
            
        with self.driver.session() as graphDB_Session:
            result  = graphDB_Session.run(query)
            result  = graphDB_Session.run(query1)
            #result  = ([record["color"] for record in result])
            #print(*result)
            return result

    def location(self):
        cql = "MATCH (x) RETURN x"
        # Execute the CQL query
        with self.driver.session() as graphDB_Session:
            nodes = graphDB_Session.run(cql)
            for node in nodes:
                print(node)
            labels = graphDB_Session.run("CALL db.labels()")
            for l in labels:
                print(l)
            relations = graphDB_Session.run("CALL db.relationshipTypes()")
            for r in relations:
                print(r)

# for testing purpose, can be commented out
if __name__ == "__main__":
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "admin"
    
    app = Recommender(uri, user, password)

    app.clearDB()
    app.createDB()
    #s = app.querygripper()
   
    #app.queryplaceposition()
    app.update('redcoins','w_20','a_130','xy_100_100','c_1','d_130')
    #app.querygripperwidth('red')
    ##app.queryangle('red')
    #s = app.queryplaceforcolor("red")
    #print(s)
    #app.querypickattrib("p42")
    #app.location()
    app.close()
    
 



