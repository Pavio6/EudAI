INSERT OR IGNORE INTO users (user_id, username, sen_profile, tts_enabled, high_contrast)
VALUES
  (1, 'demo_general', 'General supportive defaults', 1, 0),
  (2, 'demo_dyslexia', 'Dyslexia-friendly layout and TTS', 1, 1);

INSERT OR IGNORE INTO questions (question_id, subject, topic, difficulty, question_text, option_a, option_b, option_c, option_d, correct_option, explanation)
VALUES
  (1, 'Math', 'Addition', 1, 'What is 2 + 3?', '4', '5', '6', '7', 'B', '2 plus 3 equals 5.'),
  (2, 'Math', 'Addition', 1, 'What is 1 + 6?', '6', '7', '8', '9', 'B', '1 plus 6 equals 7.'),
  (3, 'Math', 'Subtraction', 1, 'What is 7 - 2?', '4', '5', '6', '7', 'B', '7 minus 2 leaves 5.'),
  (4, 'Math', 'Subtraction', 1, 'What is 9 - 4?', '4', '5', '6', '7', 'B', '9 minus 4 leaves 5.'),
  (5, 'Math', 'Addition', 1, 'What is 3 + 4?', '6', '7', '8', '9', 'B', '3 plus 4 equals 7.'),
  (6, 'Math', 'Addition', 2, 'What is 12 + 5?', '15', '16', '17', '18', 'C', '12 plus 5 equals 17.'),
  (7, 'Math', 'Subtraction', 2, 'What is 15 - 7?', '6', '7', '8', '9', 'C', '15 minus 7 equals 8.'),
  (8, 'Math', 'Addition', 2, 'What is 18 + 6?', '22', '23', '24', '25', 'C', '18 plus 6 equals 24.'),
  (9, 'Math', 'Subtraction', 2, 'What is 20 - 9?', '9', '10', '11', '12', 'B', '20 minus 9 equals 11.'),
  (10, 'Math', 'Addition', 2, 'What is 14 + 9?', '22', '23', '24', '25', 'B', '14 plus 9 equals 23.'),
  (11, 'Math', 'Addition', 3, 'What is 125 + 87?', '202', '211', '212', '213', 'C', '125 plus 87 equals 212, check place value: 5+7, 2+8, 1.'),
  (12, 'Math', 'Subtraction', 3, 'What is 340 - 128?', '202', '212', '222', '232', 'B', '340 minus 128 equals 212 by borrowing.'),
  (13, 'Math', 'Addition', 3, 'What is 267 + 145?', '402', '412', '422', '432', 'B', '267 plus 145 equals 412.'),
  (14, 'Math', 'Subtraction', 3, 'What is 580 - 267?', '303', '313', '323', '333', 'B', '580 minus 267 equals 313.'),
  (15, 'Math', 'Addition', 3, 'What is 356 + 189?', '533', '545', '545', '555', 'B', '356 plus 189 equals 545.'),
  (16, 'Math', 'Addition', 4, 'What is 1,245 + 3,678?', '4,883', '4,893', '4,923', '4,933', 'C', '1,245 plus 3,678 equals 4,923; add each column with carrying.'),
  (17, 'Math', 'Subtraction', 4, 'What is 9,002 - 4,389?', '4,513', '4,603', '4,613', '4,703', 'C', 'Borrowing across zeros leaves 4,613.'),
  (18, 'Math', 'Addition', 4, 'What is 7,456 + 2,789?', '10,145', '10,245', '10,255', '10,345', 'B', 'Add thousands, hundreds, tens, and ones to get 10,245.'),
  (19, 'Math', 'Subtraction', 4, 'What is 12,304 - 6,789?', '5,505', '5,515', '5,525', '5,535', 'B', '12,304 minus 6,789 equals 5,515.'),
  (20, 'Math', 'Subtraction', 4, 'What is 8,120 - 2,987?', '5,123', '5,133', '5,143', '5,153', 'B', '8,120 minus 2,987 equals 5,133.'),
  (21, 'Math', 'Addition', 5, 'What is 23,457 + 56,789?', '80,146', '80,236', '80,246', '80,256', 'C', 'Summing each place yields 80,246.'),
  (22, 'Math', 'Subtraction', 5, 'What is 90,005 - 47,869?', '42,036', '42,126', '42,136', '42,146', 'C', 'Borrow carefully to get 42,136.'),
  (23, 'Math', 'Addition', 5, 'What is 345,678 + 123,456?', '468,134', '468,234', '469,134', '469,234', 'C', 'Add hundreds of thousands through ones to reach 469,134.'),
  (24, 'Math', 'Subtraction', 5, 'What is 503,210 - 287,654?', '215,446', '215,556', '215,566', '215,576', 'B', 'Subtract each place with regrouping: 503,210 - 287,654 = 215,556.'),
  (25, 'Math', 'Addition', 5, 'What is 789,321 + 654,987?', '1,434,108', '1,444,108', '1,444,308', '1,444,908', 'C', '789,321 plus 654,987 equals 1,444,308.');
