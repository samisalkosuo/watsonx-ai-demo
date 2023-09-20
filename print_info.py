#print info about this 
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes, DecodingMethods


print("watsonx.ai demo")
print()
print("Models that can be used with MODEL_ID environment variable:")
models=ModelTypes._member_map_
for model in models:    
    print(f"{model}: {models[model].value}")
print()
