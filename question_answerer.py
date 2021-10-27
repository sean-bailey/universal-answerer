"""
contain functions for answering questions based on text


"""
from transformers import pipeline

mainmodel="mrm8488/bert-tiny-finetuned-squadv2"
maintokenizer="mrm8488/bert-tiny-finetuned-squadv2"
qa_pipeline = pipeline(
    "question-answering",
    model=mainmodel,
    tokenizer=maintokenizer
)
def answer_question(question,context):

    return qa_pipeline({
        'context':context,
        'question':question
    })['answer']

