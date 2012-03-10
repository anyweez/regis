use regis;

ALTER TABLE models_question_categories RENAME models_questiontemplate_categories;
ALTER TABLE models_questiontemplate_categories DROP COLUMN question_id;
ALTER TABLE models_questiontemplate_categories ADD questiontemplate_id int(11) NOT NULL;
