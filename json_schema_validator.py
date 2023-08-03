
from typing import Union

json_schema={
           
               # Write your
               # JSON SCHEMA
               # here
            
        }
  

json_data={
            # 
            #    Write your
            #    JSON DATA
            #    here
            # 
   }

def _validate_maximum_minimum_exmax_exmin(json_data: Union[str, int, bool], conditions: dict[str, Union[int, str]]) -> bool:
   """Method will validate the below properties of json json_schema
   1. MINIMUM
   2. MAXIMUM
   3. EXCLUSIVE_MINIMUM
   4. EXCLUSIVE_MAXIMUM
   """

   is_valid: bool = True
   if conditions['minimum'] is not None:
      is_valid &= (json_data >= conditions['minimum'])
   if conditions['maximum'] is not None:
      is_valid &= (json_data <= conditions['maximum'])
   if conditions['exclusiveMinimum'] is not None:
      is_valid &= (json_data > conditions['exclusiveMinimum'])
   if conditions['exclusiveMaximum'] is not None:
      is_valid &= (json_data < conditions['exclusiveMaximum'])
   return is_valid

def integer_maximum_minimum_check(json_data,json_schema):
   """This method checks 
      whether integer is 
      within the given range
    """
   conditions: dict[str, Union[str, int, float]] = {
      "minimum": json_schema.get("minimum"),
      "maximum": json_schema.get("maximum"),
      "exclusiveMinimum": json_schema.get("exclusiveMinimum"),
      "exclusiveMaximum": json_schema.get("exclusiveMaximum"),
   }
   return _validate_maximum_minimum_exmax_exmin()(json_data, conditions)



def enum_check(json_schema,json_data):
    """"
    checks for enum 
    key word is there
    in the schema
    """
    if "enum" in json_schema:
      if json_data in json_schema["enum"]:
         return True
      else:
         return False
    else:
         return True 
    


def min_max_proproperties_check(json_schema,json_data):
    """
    checks for number 
    of properties 
    in the schema
    """
    if "minProperties" in json_schema and "maxProperties" in json_schema:
        return  len(json_data)>=json_schema["minProperties"] and len(json_data)<=json_schema["maxProperties"]
    elif "minProperties" in json_schema:
        return  len(json_data)>=json_schema["minProperties"]
    elif"maxProperties" in json_schema:
        return len(json_data)<=json_schema["maxProperties"]
    



def required_list_check(json_schema,json_data,key):
   """
   checks properties against
   required list
   """
   if "required" in json_schema:
       if key in json_schema["required"]:
          return True
       else:
          return False
   else:
      return True
   



def check_allOf_anyOf_oneOf(json_schema,json_data):
   """
   checks for allOf
   anyOf and oneOf conditions
   """
   if "anyOf" in json_schema:
         is_condition_satisfied: bool = False
         for inner_json_schema in json_schema["anyOf"]:
            is_condition_satisfied |= (json_schema_validator(inner_json_schema,json_data))
         return is_condition_satisfied
   elif "allOf" in json_schema:
         is_condition_satisfied: bool = True
         for inner_json_schema in json_schema["allOf"]:
            is_condition_satisfied &= (json_schema_validator(inner_json_schema,json_data))
         return is_condition_satisfied
   elif "oneOf" in json_schema:
         is_condition_satisfied = 0
         for inner_json_schema in json_schema["oneOf"]:
            is_condition_satisfied += (json_schema_validator(inner_json_schema,json_data))
         if is_condition_satisfied==1:
             return True
         else:
             return False
         


   
def json_schema_validator(json_schema, json_data):
    
    #main method foe schema validator
      print(json_schema)
      try:
            if json_schema["type"]=="object":   #if data is of object type
               if "anyOf" in json_schema or "oneOf" in json_schema or "allOf" in json_schema:# check for anyOf/allOf/oneOf
                  return check_allOf_anyOf_oneOf(json_schema,json_data) 
               else:
                  if min_max_proproperties_check(json_schema,json_data):#check for min/max properties
                     for key in json_schema["properties"]:#checking for subschemas
                        if isinstance(json_schema["properties"][key],dict) and required_list_check(json_schema,json_data,key) :
                                 try:
                                    if json_schema_validator(json_schema["properties"][key],json_data[key]):#if subschema goto main method again
                                       continue
                                    else:
                                       return False
                                 except:
                                    return False
                        else:
                           continue
                     return True
                  else:
                     return False
                     
            elif json_schema["type"]=="string":#if data is of string type
               if isinstance(json_data,str):
                     return enum_check(json_schema,json_data)
               else:
                  return False  
            elif json_schema["type"]=="integer":#if data is of integer type
               if isinstance(json_data,int):
                     return integer_maximum_minimum_check(json_data,json_schema) and enum_check(json_schema,json_data)
               else:
                  return False 
            elif json_schema["type"]=="boolean":#if data is of boolean type
               if isinstance(json_data,bool):
                     return True
            elif json_schema["type"]=="number":#if data is ofnumber type
               if isinstance(json_data,int) or isinstance(json_data,float):
                     return integer_maximum_minimum_check(json_data,json_schema) and enum_check(json_schema,json_data)
      except:
          return True        


   #printing result        
val=json_schema_validator(json_schema,json_data) 



if val:
   print("Json_data is valid against given Json_schema")
else:
   print("Json_data is not valid against given Json_schema")
