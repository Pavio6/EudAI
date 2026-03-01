INSERT OR IGNORE INTO questions (
  question_id, subject, topic, difficulty, question_text,
  option_a, option_b, option_c, option_d, correct_option, explanation
)
VALUES
  (1001, 'English', 'Vocabulary', 1, 'Choose the synonym of "happy".', 'sad', 'glad', 'angry', 'tired', 'B', 'Glad means happy.'),
  (1002, 'English', 'Vocabulary', 1, 'Choose the antonym of "big".', 'small', 'huge', 'wide', 'high', 'A', 'Small is the opposite of big.'),
  (1003, 'English', 'Grammar', 1, 'She ___ to school every day.', 'go', 'goes', 'going', 'gone', 'B', 'Use "goes" for third-person singular in present simple.'),
  (1004, 'English', 'Grammar', 1, 'They ___ playing football now.', 'is', 'am', 'are', 'be', 'C', 'Use "are" with "they".'),
  (1005, 'English', 'Reading', 1, 'What punctuation ends a question?', 'comma', 'period', 'question mark', 'semicolon', 'C', 'A question ends with a question mark.'),
  (1006, 'English', 'Vocabulary', 1, 'Choose the correct plural form: one child, two ___.', 'childs', 'children', 'childes', 'childrens', 'B', 'The irregular plural of child is children.'),
  (1007, 'English', 'Grammar', 1, 'I ___ a book yesterday.', 'read', 'reads', 'reading', 'am read', 'A', 'Past simple form is read.'),
  (1008, 'English', 'Vocabulary', 1, 'Pick the word that names a color.', 'run', 'blue', 'quickly', 'sing', 'B', 'Blue is a color.'),

  (1009, 'English', 'Vocabulary', 2, 'Choose the synonym of "begin".', 'finish', 'start', 'stop', 'break', 'B', 'Start means begin.'),
  (1010, 'English', 'Grammar', 2, 'If it rains, we ___ at home.', 'stay', 'stays', 'stayed', 'staying', 'A', 'Use base verb in first conditional after "we".'),
  (1011, 'English', 'Grammar', 2, 'He ___ TV when I called.', 'watches', 'watched', 'was watching', 'is watching', 'C', 'Past continuous fits an interrupted action in the past.'),
  (1012, 'English', 'Reading', 2, 'Which sentence is correct?', 'She do homework.', 'She does homework.', 'She doing homework.', 'She done homework.', 'B', 'Third-person singular needs "does".'),
  (1013, 'English', 'Vocabulary', 2, 'Choose the antonym of "early".', 'soon', 'late', 'quick', 'fast', 'B', 'Late is the opposite of early.'),
  (1014, 'English', 'Grammar', 2, 'There ___ many books on the table.', 'is', 'are', 'was', 'be', 'B', 'Use "are" with plural noun "books".'),
  (1015, 'English', 'Reading', 2, 'What is the main idea of a paragraph?', 'A tiny detail', 'The central point', 'The title only', 'The final word', 'B', 'Main idea is the central point.'),
  (1016, 'English', 'Vocabulary', 2, 'Choose the best word: "The movie was very ___."', 'interesting', 'interest', 'interestedly', 'interests', 'A', 'Use adjective "interesting" to describe a movie.'),

  (1017, 'English', 'Grammar', 3, 'By next year, she ___ here for five years.', 'works', 'worked', 'will have worked', 'has work', 'C', 'Future perfect: will have + past participle.'),
  (1018, 'English', 'Vocabulary', 3, 'Choose the synonym of "rapid".', 'slow', 'quick', 'weak', 'calm', 'B', 'Rapid means quick.'),
  (1019, 'English', 'Grammar', 3, 'Neither Tom nor his friends ___ coming.', 'is', 'are', 'was', 'be', 'B', 'Verb agrees with nearest plural subject "friends".'),
  (1020, 'English', 'Reading', 3, 'Which is an inference?', 'A stated fact', 'A guess based on clues', 'A page number', 'A definition only', 'B', 'Inference means drawing a conclusion from evidence.'),
  (1021, 'English', 'Grammar', 3, 'If I ___ more time, I would travel.', 'have', 'had', 'will have', 'am having', 'B', 'Second conditional uses past simple in the if-clause.'),
  (1022, 'English', 'Vocabulary', 3, 'Choose the antonym of "expand".', 'grow', 'spread', 'contract', 'increase', 'C', 'Contract is the opposite of expand.'),
  (1023, 'English', 'Reading', 3, 'A thesis statement usually appears in the ___.', 'conclusion', 'introduction', 'appendix', 'footnote', 'B', 'It is usually in the introduction.'),
  (1024, 'English', 'Grammar', 3, 'She asked me where I ___.', 'am going', 'was going', 'go', 'will go', 'B', 'Backshift in reported speech: was going.'),

  (1025, 'English', 'Grammar', 4, 'Hardly had we arrived when it ___.', 'rains', 'rain', 'rained', 'was rain', 'C', 'Past simple is correct in this structure.'),
  (1026, 'English', 'Vocabulary', 4, 'Choose the closest meaning of "meticulous".', 'careless', 'very careful', 'angry', 'noisy', 'B', 'Meticulous means very careful about details.'),
  (1027, 'English', 'Grammar', 4, 'No sooner ___ the door than the phone rang.', 'I opened', 'did I open', 'I open', 'do I open', 'B', 'Inversion is required: did I open.'),
  (1028, 'English', 'Reading', 4, 'What best describes a persuasive text?', 'It tells a story only', 'It explains lab steps', 'It argues to convince readers', 'It lists random facts', 'C', 'Persuasive writing aims to convince readers.'),
  (1029, 'English', 'Vocabulary', 4, 'Choose the antonym of "scarce".', 'rare', 'abundant', 'limited', 'insufficient', 'B', 'Abundant is the opposite of scarce.'),
  (1030, 'English', 'Grammar', 4, 'If he ___ earlier, he would have caught the train.', 'left', 'leaves', 'had left', 'has left', 'C', 'Third conditional uses had + past participle.'),
  (1031, 'English', 'Reading', 4, 'A counterargument in an essay is used to ___.', 'ignore other views', 'present and respond to opposing views', 'repeat the thesis only', 'end the essay', 'B', 'Counterarguments acknowledge and answer opposing points.'),
  (1032, 'English', 'Grammar', 4, 'The proposal, along with the reports, ___ approved.', 'were', 'are', 'was', 'have', 'C', 'Subject is singular: proposal was approved.'),

  (1033, 'English', 'Vocabulary', 5, 'Choose the best meaning of "ubiquitous".', 'rare and unusual', 'present everywhere', 'easy to break', 'hard to notice', 'B', 'Ubiquitous means present everywhere.'),
  (1034, 'English', 'Grammar', 5, 'Had she known, she ___ differently.', 'acts', 'would act', 'would have acted', 'has acted', 'C', 'Inverted third conditional: would have acted.'),
  (1035, 'English', 'Reading', 5, 'In academic writing, hedging is used to ___.', 'state claims with measured caution', 'replace all evidence', 'avoid any argument', 'add humor', 'A', 'Hedging softens certainty in claims.'),
  (1036, 'English', 'Vocabulary', 5, 'Choose the closest synonym of "ameliorate".', 'worsen', 'improve', 'remove', 'delay', 'B', 'Ameliorate means improve.'),
  (1037, 'English', 'Grammar', 5, 'Scarcely ___ the speech when the alarm sounded.', 'he had begun', 'had he begun', 'he begins', 'did he began', 'B', 'Negative adverbials require inversion: had he begun.'),
  (1038, 'English', 'Reading', 5, 'A valid conclusion should be ___.', 'unrelated to evidence', 'drawn logically from presented evidence', 'longer than the introduction only', 'purely emotional', 'B', 'Conclusions should follow from evidence.'),
  (1039, 'English', 'Vocabulary', 5, 'Choose the antonym of "concur".', 'agree', 'approve', 'disagree', 'accept', 'C', 'Concur means agree; antonym is disagree.'),
  (1040, 'English', 'Grammar', 5, 'Not only ___ the data flawed, but the method was biased.', 'was', 'were', 'is', 'be', 'A', 'With singular subject "data" as treated here, "was" is used in this item.');
