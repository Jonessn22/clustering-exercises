SELECT *
                        FROM properties_2017
                        LEFT JOIN airconditioningtype ON properties_2017.airconditioningtypeid
                        LEFT JOIN architecturalstyletype ON properties_2017.architecturalstyletypeid
                        LEFT JOIN buildingclasstype ON properties_2017.buildingclasstypeid
                        LEFT JOIN heatingorsystemtype ON properties_2017.heatingorsystemtypeid
                        LEFT JOIN propertylandusetype ON properties_2017.propertylandusetypeid
                        LEFT JOIN storytype ON properties_2017.storytypeid
                        LEFT JOIN typeconstructiontype ON properties_2017.typeconstructiontypeid
                        LEFT JOIN predictions_2017 ON properties_2017.parcelid
                        