/*
SQL QUERY TO ACQUIRE ZILLOW DATA
*/

SELECT prop.*,
# SELECT ALL FROM PROPERTIES

       pred.logerror, 
       pred.transactiondate, 
       # SELECT LOGERROR AND TRANSACTIONDATE COLUMNS FROM PREDICTIONS
       
       air.airconditioningdesc, 
       arch.architecturalstyledesc, 
       build.buildingclassdesc, 
       heat.heatingorsystemdesc, 
       landuse.propertylandusedesc, 
       story.storydesc, 
       construct.typeconstructiondesc
       #SELECT THESE COLUMNS FROM THESE TABLES

FROM   properties_2017 prop  
       INNER JOIN (SELECT parcelid,
       					  logerror,
                          Max(transactiondate) transactiondate 
                   FROM   predictions_2017
                    # THIS INNER JOIN WILL ONLY RETURN THE RESULTS OF THE TABLES IF THEY HAVE VALUES THAT MATCH TO THE OTHER
                   
                   GROUP  BY parcelid, logerror) pred
                   # THE RESULTS WILL BE GROUPED BY PARCELID (AND LOGERROR?)
               USING (parcelid) 
               # THEY WILL BE JOINED ON THE COLUMN PARCELID
               
       LEFT JOIN airconditioningtype air USING (airconditioningtypeid) 
       LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid) 
       LEFT JOIN buildingclasstype build USING (buildingclasstypeid) 
       LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid) 
       LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid) 
       LEFT JOIN storytype story USING (storytypeid) 
       LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid) 
       # THESE LEFT JOINS WILL BE ADDED TO MAIN PROPERTIES TABLE QUERY RESULT IF THEY HAVE A CORRESPONDING VALUE
       
WHERE  prop.latitude IS NOT NULL 
       AND prop.longitude IS NOT NULL AND transactiondate <= '2017-12-31'
       # THIS WILL FILTER OUT ANY RESULTS WHERE THE LAT OR LONG VALUES ARE NULL AND WHERE THE TRANS DATA WAS BEFORE 2018 ; 
       