import pandas as pd
import csv
import numpy as np
import sys

# TODO: MAKE THE PSEUDOMAIN FUNCTION ONE TAHT RETURNS THE EXCEL SHEET


def get_max_scores(clean_data, num_students):
    """
    Calculates the maximum possible score the class could've gotten per question
    Returns a dataframe of these scores
    """
    max_scores = [(int(col.split("/")[1]) * num_students) for col in clean_data.columns]
    max_scores = pd.DataFrame(max_scores, columns=["Max Score"])

    return max_scores


def get_total_scores(clean_data):
    """
    Calculates the total score the class received per question
    Returns a dataframe of these scores
    """
    total_scores = [clean_data[col].sum() for col in clean_data.columns]
    total_scores = pd.DataFrame(total_scores, columns=["Total Score"])

    return total_scores


def get_scores_by_question(raw_scores):
    """
    Returns the class average for each question
    Uses the methods from original spreadsheet to calculate class average (total score/maximum possible score)
    """
    num_students = len(raw_scores.index)

    try:
        max_scores = get_max_scores(raw_scores, num_students)
        total_scores = get_total_scores(raw_scores)
    except Exception as e:
        print("error getting scores", e)

    # Check that both have the same length
    if len(total_scores) != len(max_scores):
        raise ValueError("Both DataFrames must have the same length")

    class_score_by_question = []
    for i in range(len(total_scores)):
        score = total_scores.iloc[i, 0] / max_scores.iloc[i, 0]
        class_score_by_question.append(score)

    # Construct a new DataFrame from the scores
    result_df = pd.DataFrame(class_score_by_question, columns=["Score Ratio"])

    return result_df


def get_raw_scores(data):
    """Gets the scores from questions that are skills questions (not names or anything like that)
    Removes everything that isn't a skill question and returns the matrix of those scores.
    """

    clean = data.dropna()
    clean = clean.drop(columns=[col for col in clean.columns if "/0" in col])
    try:
        clean = clean.filter(regex="^Q. ")
    except Exception as e:
        raise ValueError(
            "The provided file does not have correctly formatted question numbers."
        )

    return clean


def get_skill_average(questions_in_skill, avg_by_question):
    """Get the average score for each question skill"""
    if (questions_in_skill == None) or ((len(questions_in_skill)) == 0):
        return None

    sum = 0
    for qnum in questions_in_skill:
        index = qnum - 1
        sum += avg_by_question["Score Ratio"][index]

    skill_average = sum / len(questions_in_skill)

    return skill_average


def score_by_skill(assessment_type, avg_by_question):
    # NOTE: THE QUESTION NUMBERS HERE MAP TO THE SCORES ONLY ! NOT INCLUDING THE NAEM
    # TODO: EDIT ALL OF THESE SO THAT THEY CORRESPOND TO THE ACTUAL NAME IN THE SPREADSHEET
    qnum_dict = {}
    if assessment_type == "ELD1_FLS":
        qnum_dict = {
            "Letter Sequence": [1, 2],
            "Identifying Vowels": [3],
            "Identifying Consonants": [4],
            "Upper-Lowercase Letters": [5, 6, 7, 8],
            "Phonics/Sound-Symbol Relationship": [9, 10],
            "Phonological Awareness: Syllables": [11, 12],
            "Phonological Awareness: Blending": [13],
            "Phonological Awareness: Segmenting": [14],
            "Phonological Awareness: Rhyming": [15, 16],
            "Phonological Awareness: First Sound": [17, 19],
            "Phonological Awareness: Last Sound": [18, 20, 21],
            "Phonological Awareness: Media Vowel Substitution": [22, 23],
            "Sentence Syntax": [24, 25],
        }
    elif assessment_type == "ELD1_CLS":
        qnum_dict = {
            "Exchanging Information and Ideas": [1, 2],
            "Interacting via Written English": [3, 4],
            "Supporting Opinions and Persuading Others": [5, 6],
            "Adapting Language Choices": [7, 8],
            "Evaluating Language Choices": [9, 10],
            "Analyzing Langugage Choices": [11, 12],
            "Listening Actively: Asking Questions": [13, 14],
            "Reading/Viewing Closely: Compare/Contrast": [15, 16],
            "Reading/Viewing Closely: Express": [17],
            "Presenting": [18, 19],
            "Writing: Using Notes": [20, 21],
            "Selecting Language Resources": [22, 23, 24],
            "Justifying/Arguing": [25, 26, 27],
        }
    elif assessment_type == "ELD1_LFC":
        qnum_dict = {
            "Understanding Text Structure": [1, 2, 3, 4],
            "Understanding Cohesion: Pronouns": [5, 6, 7, 8],
            "Understanding Cohesion: Links": [9, 10, 11],
            "Expanding and Enriching Ideas: Verbs": [12, 13, 14, 15],
            "Expanding and Enriching Ideas: Nouns": [16, 17, 18],
            "Expanding and Enriching Ideas: Details": [19, 20, 21],
            "Connecting Ideas": [22, 23, 24],
            "Condensing Ideas": [25, 26],
        }
    elif assessment_type == "ELD2_FLS":
        qnum_dict = {
            "Standard Phoneme Deletion": [1, 2],
            "Phonemic Substitution": [3, 4, 5],
            "Phoneme Addition": [6, 7],
            "Phoneme Manipulation": [8, 9],
            "Identifying Diphthongs": [10, 11, 12],
            "R-Controlled Vowels": [13, 14],
            "Spelling with Long and Short Vowel Sounds": [15, 17],
            "Frontal Phonemes/Spelling for /j/ and /s/ sounds": [18, 19],
            "Spelling Patterns - Double Consonant Words": [20, 21],
            "Spelling Patterns - Adding suffix to words with a final 'e'": [22, 23],
            "Identifying the Schwa Sound": [24, 25],
            "Prefixes - Vocabulary": [26, 27],
            "Suffixes": [28, 29],
        }
    elif assessment_type == "ELD2_CLS":
        qnum_dict = {
            "Exchanging Information and Ideas/Asking & Answering Questions": [1, 2],
            "Interacting via Written English ": [3, 4],
            "Supporting Opinions and Persuading Others": [5, 6],
            "Adapting Language Choices": [7, 8],
            "Listening Actively ": [9, 10, 11],
            "Evaluating Language Choices": [12, 14],
            "Reading/Viewing Closely": [13, 15, 16],
            "Analyzing Language Choices": [17, 18],
            "Presenting": [19, 20],
            "Writing": [21, 22],
            "Justifying/Arguing": [23, 24, 25],
            "Selecting Language Resources": [26, 27, 28],
        }
    elif assessment_type == "ELD2_LFC":
        qnum_dict = {
            "Understanding Text Structure": [1, 2, 3, 4],
            "Writing Texts with Increasingly Clear and Cohesive Statements": [
                5,
                6,
                7,
                8,
            ],
            "Pronouns": [9, 10],
            "Synonyms": [11, 12],
            "Applying Knowledge of Familiar Language Resources": [13, 14],
            "Using Nouns and Noun Phrases": [15, 16],
            "Using Verbs and Verb Phrases": [17, 18, 19, 20, 21, 22, 23],
            "Modifying to Add Details": [24, 25, 26],
            "Connecting Ideas *Complex Sentences": [27, 28],
            "Condensing Ideas": [29, 30],
        }
    scores_by_skill = {}
    for key in qnum_dict:
        score = get_skill_average(qnum_dict[key], avg_by_question)
        scores_by_skill[key] = score

    return scores_by_skill


def get_class_score(avg_by_question):
    class_score = (avg_by_question.mean())["Score Ratio"]
    return class_score


def report_from_file(filepath, assessment_type):
    df = pd.read_csv(filepath)
    raw_scores = get_raw_scores(df)
    scores_by_question = get_scores_by_question(raw_scores)

    by_skill_dict = score_by_skill(assessment_type, scores_by_question)
    overall = get_class_score(scores_by_question)

    by_skill_dict["\n"] = "\n"
    by_skill_dict["Class Score"] = overall

    skillScores = pd.DataFrame(
        list(by_skill_dict.values()),
        index=list(by_skill_dict.keys()),
        columns=["Score"],
    )

    return skillScores


if __name__ == "__main__":
    filepath = "../testingFiles/CLS1.csv"
    assessment_type = "ELD1_CLS"
    summary = report_from_file(filepath, assessment_type)
