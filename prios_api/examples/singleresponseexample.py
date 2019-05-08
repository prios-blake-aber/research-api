# Example 5 - Meeting with:
# Question: 1 Likert Question
# Participants: Two Meeting Participants who both have believability
# Responses: 1 [1]
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
    question.question_type = objects.QuestionType.LIKERT


for question in meeting.questions:
    natalie_response = objects.Response(source=natalie, target='Does this work?', value=1)
    question.responses.append(natalie_response)
