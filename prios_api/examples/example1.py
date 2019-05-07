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
