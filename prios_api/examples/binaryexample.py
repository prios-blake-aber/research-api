# Example 1 - Meeting with:
# Question: 1 Yes/No Question
# Participants: Two Meeting Participants who both have believability
# Responses: 2 (1 yes, 1 no)
# Believability: Total of 0.95 Believability in the meeting

from prios_api.domain_objects import objects

meeting = objects.Meeting(name='Test Meeting')

blake = objects.Person(name='Blake', believability=0.9)
meeting.participants.append(blake)

natalie = objects.Person(name='Natalie', believability=0.05)
meeting.participants.append(natalie)

question = objects.Question(title='Does this work?')
meeting.questions.append(question)

for question in meeting.questions:
    question.question_type = objects.QuestionType.BINARY


for question in meeting.questions:
    natalie_response = objects.Response(source=natalie, target='Does this work?', value='yes')
    question.responses.append(natalie_response)
    blake_response = objects.Response(source=blake, target='Does this work?', value='No')
    question.responses.append(blake_response)
