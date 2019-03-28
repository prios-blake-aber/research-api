
configuration = [
    ('Entity', 'GrammarObject'),  # Entities
    ('Person', 'Entity'),
    ('System', 'Entity'),

    ('Goal', 'GrammarCollection'),  # Goals
    ('Responsibility', 'Goal'),
    ('Task', 'Responsibility'),

    ('Meeting', 'GrammarCollection'),  # Other Collections
    ('Team', 'GrammarCollection'),
    ('Location', 'GrammarCollection'),
    ('Project', 'GrammarCollection'),
    ('TimeWindow', 'GrammarCollection'),
    ('Taxonomy', 'GrammarCollection'),

    ('Measure', 'GrammarObject'),  # Measures
    ('Quality', 'Measure'),
    ('Believability', 'Measure'),
    ('Outcome', 'Measure'),

    ('Attribute', 'Quality'),  # Qualities
    ('Value', 'Quality'),
    ('Interest', 'Quality'),
    ('Skill', 'Quality'),

    ('IssueLog', 'Outcome'),  # Outcome

    ('Assessment', 'GrammarAssertion'),  # Assessments
    ('Dot', 'Assessment'),
    ('Ranking', 'Assessment'),
    ('Test', 'Assessment'),
    ('Review', 'Assessment'),

    ('Estimation', 'GrammarAssertion'),  # Estimations
    ('Resume', 'Estimation'),
    ('Stream', 'Estimation'),

    ('Intervention', 'GrammarAssertion'),  # Interventions
    ('PopUp', 'Intervention'),
    ('Training', 'Intervention'),

    ('Reward', 'GrammarAssertion'),  # Rewards
    ('Extrinsic', 'Reward'),
    ('Intrinsic', 'Reward')
]


