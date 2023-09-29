from src.schemas import Configuration
import json
import re
import streamlit as st
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import (
    ModelTypes,
    DecodingMethods,
)


class Engine:
    def __init__(self):
        self._config = Configuration()
        with open("config.json", "r") as file:
            self.json_config = json.load(file)
        self.claims = self.json_config["inputData"]

    def generateText(self, prompt: str, generate_params: list) -> str:
        model = Model(
            model_id=ModelTypes[self._config.model_id],
            params=generate_params,
            credentials={
                "apikey": self._config.ibm_api_key,
                "url": self._config.ibm_ai_api_endpoint,
            },
            project_id=self._config.project_id,
        )
        generated_response = model.generate(prompt=prompt)
        self.__debug_print(f"PROMPT:\n{prompt}")
        self.__debug_print(f"RESPONSE:\n{generated_response}")
        self.__debug_print("")
        generatedText = generated_response["results"][0]["generated_text"]
        return generatedText

    def __debug_print(self, obj):
        if self._config.debug_print == "true":
            print(obj)

    def __parse_enumerated_list(self, string):
        try:
            pattern = r"\d+\.\s+"
            string = re.sub(pattern, "####", string)
            items = string.split("####")
            return [item.strip() for item in items if item != ""]
        except Exception as e:
            return None

    def __parse_entities(self, string):
        try:            
            entities = {
                f'{self.json_config["entity1HeaderText"]}': f'{self.json_config["entity1DefaultValueText"]}',
                f'{self.json_config["entity2HeaderText"]}': f'{self.json_config["entity2DefaultValueText"]}',
                f'{self.json_config["entity3HeaderText"]}': f'{self.json_config["entity3DefaultValueText"]}',
                f'{self.json_config["entity4HeaderText"]}': f'{self.json_config["entity4DefaultValueText"]}',
            }
            lines = string.split(";")
            for line in lines:
                parts = line.split(":")
                # if len(parts) != 2:
                #     raise Exception("Invalid format: ", string)
                key = parts[0].strip()
                value = parts[1].strip()
                entities[key] = value
            return entities
        except Exception as e:
            return None


    def query_bam_entities(self, prompt: str) -> str:
        try:
            result = None
            generate_params = {
                GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 1,
                GenParams.TOP_K: 50,
                GenParams.MIN_NEW_TOKENS: 1,
                GenParams.MAX_NEW_TOKENS: 50,
            }
            inputPrompt = self.json_config["promptEntities"]
            inputPrompt = inputPrompt.replace("ENTITY1",self.json_config["entity1HeaderText"])
            inputPrompt = inputPrompt.replace("ENTITY2",self.json_config["entity2HeaderText"])
            inputPrompt = inputPrompt.replace("ENTITY3",self.json_config["entity3HeaderText"])
            inputPrompt = inputPrompt.replace("ENTITY4",self.json_config["entity4HeaderText"])
            inputPrompt = inputPrompt.replace("INPUTTEXT",prompt)
            #inputText = f"Read this Insurance claim description and extract the Car make and model, Location of the incident like street and date time if there is any mentioned. If you don't find these details in the description, please fill it as Not Found. input: A car accident occurred on Jan 1st, 2023 at 5pm at the intersection of woodbridge. The insured vehicle, a Honda Civic, was hit by another vehicle that ran a red light. The insured driver, John, was driving within the speed limit and following all traffic rules. The accident resulted in significant damage to the insured vehicle, including a broken bumper and damaged front fender. There were no injuries reported. The insured is filing a claim for the repairs and any necessary medical expenses. output: {self.json_config['entity1HeaderText']}: Honda Civic;{self.json_config['entity2HeaderText']}: Woodbridge; {self.json_config['entity3HeaderText']}: Jan 1st, 2023; {self.json_config['entity4HeaderText']}: 5pm. input: The insured vehicle, a Ford RAM, was stolen from Boston on Dec 2nd 2022. The vehicle was parked in a secure parking lot, and all necessary precautions were taken, such as locking the doors and activating the alarm system. The insured immediately reported the theft to the police and obtained a police report. The vehicle had comprehensive insurance coverage, and the insured is filing a claim for the stolen vehicle, including its estimated value, accessories, and personal belongings that were inside the vehicle at the time of theft. output: {self.json_config['entity1HeaderText']}: Ford RAM; {self.json_config['entity2HeaderText']}: Boston; {self.json_config['entity3HeaderText']}: Dec 2nd 2022; {self.json_config['entity4HeaderText']}: Not Found. input: The insured vehicle, a Tesla model X, was vandalized on march 23rd while parked in front of the insured's residence on Magador Street. The vandalism included scratched paint, broken windows, and damage to the side mirrors. The insured promptly reported the incident to the police and obtained a police report. The insured is filing a claim for the repairs and any necessary replacement parts. The estimated cost of repairs has been assessed by a reputable auto repair shop. output: {self.json_config['entity1HeaderText']}: Tesla Model X; {self.json_config['entity2HeaderText']}: Magador Street; {self.json_config['entity3HeaderText']}: march 23rd; {self.json_config['entity4HeaderText']}: Not Found. input: The insured vehicle, was parked outside during a severe hailstorm. As a result, the vehicle suffered extensive hail damage, including dents on the roof, hood, and trunk. The insured promptly reported the incident and is filing a claim for the necessary repairs. The estimated cost of repairs has been assessed by an authorized auto repair shop. Managed entities: {self.json_config['entity1HeaderText']}: Not Found; {self.json_config['entity2HeaderText']}: Parked outside; {self.json_config['entity3HeaderText']}: Not Found; {self.json_config['entity4HeaderText']}: Not Found. input: While driving on Anthony Street on 1st June, the insured vehicle, a BMW Q1, collided with a large animal (e.g., deer) that suddenly crossed the road. The accident resulted in damage to the front bumper, grille, and headlights. The insured promptly reported the incident and is filing a claim for the repairs. Additionally, the insured sought medical attention for any potential injuries resulting from the collision. output: {self.json_config['entity1HeaderText']}: BMW Q1; {self.json_config['entity2HeaderText']}: Anthony Street; {self.json_config['entity3HeaderText']}: 1st June; {self.json_config['entity4HeaderText']}: Not Found. input: The insured vehicle, caught fire on april 1st due to a mechanical malfunction. The fire resulted in significant damage to the vehicle, including damage to the engine, interior, and exterior. The insured immediately contacted the fire department, and the incident was reported to the police. The insured is filing a claim for the repairs and is providing the fire department report as evidence of the fire incident. output: {self.json_config['entity1HeaderText']}: Not Found; {self.json_config['entity2HeaderText']}: Not Found; {self.json_config['entity3HeaderText']}: April 1st, 2023; {self.json_config['entity4HeaderText']}: Not Found. input: {prompt}. output:"
            result = self.generateText(inputPrompt,generate_params)            
        except Exception as e:
            print(e)
            result = None
        return result

    def query_bam_next_steps(self, prompt: str) -> str:
        try:
            prompt = prompt.strip()
            prompt = prompt.replace("\n", " ")

            generate_params = {
                GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 1,
                GenParams.TOP_K: 50,
                GenParams.MIN_NEW_TOKENS: 1,
                GenParams.MAX_NEW_TOKENS: 500,
                GenParams.RANDOM_SEED: 1050
            }
            inputPrompt = self.json_config["promptNextSteps"]
            inputPrompt = inputPrompt.replace("INPUTTEXT",prompt)
            result = self.generateText(inputPrompt,generate_params)
        except Exception as e:
            print(e)
            result = None
        return result

    def query_bam_summary(self, prompt: str) -> str:
        try:
            generate_params = {
                GenParams.DECODING_METHOD: DecodingMethods.SAMPLE,
                GenParams.TEMPERATURE: 0.7,
                GenParams.TOP_P: 1,
                GenParams.TOP_K: 50,
                GenParams.REPETITION_PENALTY: 2,
                GenParams.MIN_NEW_TOKENS: 5,
                GenParams.MAX_NEW_TOKENS: 25,
                GenParams.RANDOM_SEED: 1050,
            }
            inputPrompt = self.json_config["promptSummary"]
            inputPrompt = inputPrompt.replace("INPUTTEXT",prompt)
            result = self.generateText(inputPrompt, generate_params)
        except Exception as e:
            print(e)
            result = None
        return result

    def query_bam(self, prompt: str):
        entities = self.query_bam_entities(prompt)
        if entities is not None:
            entities = self.__parse_entities(entities)
        next_steps = self.query_bam_next_steps(prompt)
        if next_steps is not None:
            next_steps = self.__parse_enumerated_list(next_steps)
        summary = self.query_bam_summary(prompt)
        return entities, next_steps, summary

    def query_entities(self, prompt: str):
        entities = self.query_bam_entities(prompt)
        if entities is not None:
            entities = self.__parse_entities(entities)
        return entities

    def query_summary(self, prompt: str):
        summary = self.query_bam_summary(prompt)
        return summary

    def query_next_steps(self, prompt: str):
        next_steps = self.query_bam_next_steps(prompt)
        if next_steps is not None:
            next_steps = self.__parse_enumerated_list(next_steps)
        return next_steps
