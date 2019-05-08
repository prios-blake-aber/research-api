# Example 4 - Meeting with:
# Question: 1 Categorical Question
# Participants: 4 Meeting Participants, 0 who have believability
# Responses: 4 total ['Give up', 'Push Ahead and see what happens', 'Delay', 'Do whatever it takes to make it work']
# Believability: 0 Believability in the meeting

from prios_api.domain_objects import objects

meeting = objects.Meeting(name='Test Meeting')

blake = objects.Person(name='Blake', believability=0.3)
meeting.participants.append(blake)

natalie = objects.Person(name='Natalie', believability=0.25)
meeting.participants.append(natalie)

will = objects.Person(name='Will', believability=0.3)
meeting.participants.append(will)

chintan = objects.Person(name='Chintan', believability=0)
meeting.participants.append(chintan)

question = objects.Question(title='How should we move forward with this project?')
meeting.questions.append(question)

for question in meeting.questions:
    question.question_type = objects.QuestionType.CATEGORICAL

for question in meeting.questions:
    natalie_response = objects.Response(source=natalie, target='How is this project going?', value='Give up')
    question.responses.append(natalie_response)
    blake_response = objects.Response(source=blake, target='How is this project going?', value='Delay')
    question.responses.append(blake_response)
    will_response = objects.Response(source=will, target='How is this project going?',
                                     value='Push Ahead and see what happens')
    question.responses.append(will_response)
    chintan_response = objects.Response(source=chintan, target='How is this project going?',
                                        value='Do whatever it takes to make it work')
    question.responses.append(chintan_response)
