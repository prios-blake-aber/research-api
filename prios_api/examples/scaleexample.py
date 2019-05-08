# Example 3 - Meeting with:
# Question: 1 1-10 Scale Question
# Participants: 3 Meeting Participants, 3 who have believability
# Responses: 3 total [7, 6, 7]
# Believability: Total of 0.85 Believability in the meeting

from prios_api.domain_objects import objects

meeting = objects.Meeting(name='Test Meeting')

blake = objects.Person(name='Blake', believability=0.3)
meeting.participants.append(blake)

natalie = objects.Person(name='Natalie', believability=0.25)
meeting.participants.append(natalie)

will = objects.Person(name='Will', believability=0.3)
meeting.participants.append(will)

question = objects.Question(title='How is this project going?')
meeting.questions.append(question)

for question in meeting.questions:
    question.question_type = objects.QuestionType.SCALE

for question in meeting.questions:
    natalie_response = objects.Response(source=natalie, target='How is this project going?', value=7)
    question.responses.append(natalie_response)
    blake_response = objects.Response(source=blake, target='How is this project going?', value=7)
    question.responses.append(blake_response)
    will_response = objects.Response(source=will, target='How is this project going?', value=7)
    question.responses.append(will_response)

values_and_weights = [(response.value, response.source.believability) for response in question.responses]
