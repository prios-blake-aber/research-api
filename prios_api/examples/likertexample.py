# Example 2 - Meeting with:
# Question: 1 Likert Question
# Participants: 5 Meeting Participants, 3 who have believability
# Responses: 5 total [1, 2, 3, 4, 4]
# Believability: Total of 0.51 Believability in the meeting

from prios_api.domain_objects import objects

meeting = objects.Meeting(name='Test Meeting')

blake = objects.Person(name='Blake', believability=0.2)
meeting.participants.append(blake)

natalie = objects.Person(name='Natalie', believability=0.01)
meeting.participants.append(natalie)

will = objects.Person(name='Will', believability=0.3)
meeting.participants.append(will)

chintan = objects.Person(name='Chintan', believability=0)
meeting.participants.append(chintan)

sophia = objects.Person(name='Sophia', believability=0)
meeting.participants.append(sophia)

question = objects.Question(title='How is this project going?')
meeting.questions.append(question)

for question in meeting.questions:
    question.question_type = objects.QuestionType.LIKERT

for question in meeting.questions:
    natalie_response = objects.Response(source=natalie, target='How is this project going?', value=1)
    question.responses.append(natalie_response)
    blake_response = objects.Response(source=blake, target='How is this project going?', value=2)
    question.responses.append(blake_response)
    will_response = objects.Response(source=will, target='How is this project going?', value=4)
    question.responses.append(will_response)
    chintan_response = objects.Response(source=chintan, target='How is this project going?', value=4)
    question.responses.append(chintan_response)
    sophia_response = objects.Response(source=sophia, target='How is this project going?', value=3)
    question.responses.append(sophia_response)

