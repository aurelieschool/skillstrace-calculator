import pandas as pd
import csv
import numpy as np
import sys


# there are some lesson/skill mappings that have been commented out because
# they're grouped in some parts of the template spreadsheet but not in others


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
            "Letter Sequence": {"Lesson": "FLS: Lesson 1", "Questions": [1, 2]},
            "Identifying Vowels and Consonants": {
                "Lesson": "FLS: Lesson 1",
                "Questions": [3, 4],
            },
            # "Identifying Consonants": [4],
            "Upper-Lowercase Letters": {
                "Lesson": "FLS: Lesson 2",
                "Questions": [5, 6, 7, 8],
            },
            "Phonics/Sound-Symbol Relationship": {
                "Lesson": "FLS: Lesson 3",
                "Questions": [9, 10],
            },
            "Phonological Awareness: Syllables": {
                "Lesson": "FLS: Lesson 8",
                "Questions": [11, 12],
            },
            "Phonological Awareness: Blending and Segmenting": {
                "Lesson": "FLS: Lesson 5",
                "Questions": [13, 14],
            },
            # "Phonological Awareness: Segmenting": [14],
            "Phonological Awareness: Rhyming": {
                "Lesson": "FLS: Lesson 7",
                "Questions": [15, 16],
            },
            "Phonological Awareness: First and Last Sounds": {
                "Lesson": "FLS: Lesson 4",
                "Questions": [17, 19, 18, 20, 21],
            },
            # "Phonological Awareness: Last Sound": [18, 20, 21],
            "Phonological Awareness: Media Vowel Substitution": {
                "Lesson": "FLS: Lesson 6",
                "Questions": [22, 23],
            },
            "Sentence Syntax": {"Lesson": "FLS: Lesson 9", "Questions": [24, 25]},
        }
    elif assessment_type == "ELD1_CLS":
        qnum_dict = {
            "Exchanging Information and Ideas/Asking & Answering Questions": {
                "Lesson": "CLS: Lesson 1",
                "Questions": [1, 2],
            },
            "Interacting via Written English": {
                "Lesson": "CLS: Lesson 2",
                "Questions": [3, 4],
            },
            "Supporting Opinions and Persuading Others": {
                "Lesson": "CLS: Lesson 3",
                "Questions": [5, 6],
            },
            "Adapting Language Choices": {
                "Lesson": "CLS: Lesson 4",
                "Questions": [7, 8],
            },
            "Evaluating Language Choices": {
                "Lesson": "CLS: Lesson 7",
                "Questions": [9, 10],
            },
            "Analyzing Langugage Choices": {
                "Lesson": "CLS: Lesson 8",
                "Questions": [11, 12],
            },
            "Listening Actively: Asking Questions": {
                "Lesson": "CLS: Lesson 5",
                "Questions": [13, 14],
            },
            "Reading/Viewing Closely: Compare/Contrast and Expressing Inferences/Conclusions": {
                "Lesson": "CLS: Lesson 6",
                "Questions": [15, 16, 17],
            },
            # "Reading/Viewing Closely: Express": [17],
            "Presenting": {"Lesson": "CLS: Lesson 9", "Questions": [18, 19]},
            "Writing: Using Notes or Graphic Organizers": {
                "Lesson": "CLS: Lesson 10",
                "Questions": [20, 21],
            },
            "Selecting Language Resources: Use Knowledge of Morphology": {
                "Lesson": "CLS: Lesson 11",
                "Questions": [22, 23, 24],
            },
            "Justifying/Arguing": {
                "Lesson": "CLS: Lesson 12",
                "Questions": [25, 26, 27],
            },
        }
    elif assessment_type == "ELD1_LFC":
        qnum_dict = {
            "Understanding Text Structure": {
                "Lesson": "LFC: Lesson 1",
                "Questions": [1, 2, 3, 4],
            },
            "Understanding Cohesion: Pronouns": {
                "Lesson": "LFC: Lesson 2",
                "Questions": [5, 6, 7, 8],
            },
            "Understanding Cohesion: How Events, Ideas, or Reasons are Linked": {
                "Lesson": "LFC: Lesson 2",
                "Questions": [9, 10, 11],
            },
            "Expanding and Enriching Ideas *Using Verbs and Verb Tenses": {
                "Lesson": "LFC: Lesson 3",
                "Questions": [12, 13, 14, 15],
            },
            "Expanding and Enriching Ideas *Using Nouns and Noun Phrases": {
                "Lesson": "LFC: Lesson 4",
                "Questions": [16, 17, 18],
            },
            "Expanding and Enriching Ideas *Modifying to Add Details": {
                "Lesson": "LFC: Lesson 5",
                "Questions": [19, 20, 21],
            },
            "Connecting Ideas": {"Lesson": "LFC: Lesson 6", "Questions": [22, 23, 24]},
            "Condensing Ideas": {"Lesson": "LFC: Lesson 7", "Questions": [25, 26]},
        }
    elif assessment_type == "ELD2_FLS":
        qnum_dict = {
            "Standard Phoneme Deletion": {
                "Lesson": "FLS: Lesson 1",
                "Questions": [1, 2],
            },
            "Phonemic Substitution": {
                "Lesson": "FLS: Lesson 2",
                "Questions": [3, 4, 5],
            },
            "Phoneme Addition": {"Lesson": "FLS: Lesson 3", "Questions": [6, 7]},
            "Phoneme Manipulation": {"Lesson": "FLS: Lesson 4", "Questions": [8, 9]},
            "Identifying Diphthongs": {
                "Lesson": "FLS: Lesson 7",
                "Questions": [10, 11, 12],
            },
            "R-Controlled Vowels": {"Lesson": "FLS: Lesson 8", "Questions": [13, 14]},
            "Spelling with Long and Short Vowel Sounds": {
                "Lesson": "FLS: Lesson 5",
                "Questions": [15, 17],
            },
            "Frontal Phonemes/Spelling for /j/ and /s/ sounds": {
                "Lesson": "FLS: Lesson 9",
                "Questions": [18, 19],
            },
            "Spelling Patterns: Double Consonant Words": {
                "Lesson": "FLS: Lesson 13",
                "Questions": [20, 21],
            },
            "Spelling Patterns: Adding suffix to words with a final 'e'": {
                "Lesson": "FLS: Lesson 12",
                "Questions": [22, 23],
            },
            "Identifying the Schwa Sound": {
                "Lesson": "FLS: Lesson 6",
                "Questions": [24, 25],
            },
            "Prefixes - Vocabulary": {
                "Lesson": "FLS: Lesson 10",
                "Questions": [26, 27],
            },
            "Suffixes": {"Lesson": "FLS: Lesson 11", "Questions": [28, 29]},
        }
    elif assessment_type == "ELD2_CLS":
        qnum_dict = {
            "Exchanging Information and Ideas/Asking & Answering Questions": {
                "Lesson": "CLS: Lesson 1",
                "Questions": [1, 2],
            },
            "Interacting via Written English ": {
                "Lesson": "CLS: Lesson 2",
                "Questions": [3, 4],
            },
            "Supporting Opinions and Persuading Others": {
                "Lesson": "CLS: Lesson 3",
                "Questions": [5, 6],
            },
            "Adapting Language Choices": {
                "Lesson": "CLS: Lesson 4",
                "Questions": [7, 8],
            },
            "Listening Actively ": {
                "Lesson": "CLS: Lesson 5",
                "Questions": [9, 10, 11],
            },
            "Evaluating Language Choices": {
                "Lesson": "CLS: Lesson 7",
                "Questions": [12, 14],
            },
            "Reading/Viewing Closely": {
                "Lesson": "CLS: Lesson 6",
                "Questions": [13, 15, 16],
            },
            "Analyzing Language Choices": {
                "Lesson": "CLS: Lesson 8",
                "Questions": [17, 18],
            },
            "Presenting": {"Lesson": "CLS: Lesson 10", "Questions": [19, 20]},
            "Writing": {"Lesson": "CLS: Lesson 9", "Questions": [21, 22]},
            "Justifying/Arguing": {
                "Lesson": "CLS: Lesson 11",
                "Questions": [23, 24, 25],
            },
            "Selecting Language Resources": {
                "Lesson": "CLS: Lesson 12",
                "Questions": [26, 27, 28],
            },
        }
    elif assessment_type == "ELD2_LFC":
        qnum_dict = {
            "Understanding Text Structure": {
                "Lesson": "LFC: Lesson 1",
                "Questions": [1, 2, 3, 4],
            },
            "Writing Texts with Increasingly Clear and Cohesive Statements": {
                "Lesson": "LFC: Lesson 2",
                "Questions": [
                    5,
                    6,
                    7,
                    8,
                ],
            },
            "Pronouns": {"Lesson": "LFC: Lesson 2", "Questions": [9, 10]},
            "Synonyms": {"Lesson": "LFC: Lesson 2", "Questions": [11, 12]},
            "Applying Knowledge of Familiar Language Resources": {
                "Lesson": "LFC: Lesson 3",
                "Questions": [13, 14],
            },
            "Using Nouns and Noun Phrases": {
                "Lesson": "LFC: Lesson 4",
                "Questions": [15, 16],
            },
            "Using Verbs and Verb Phrases": {
                "Lesson": "LFC: Lesson 3",
                "Questions": [17, 18, 19, 20, 21, 22, 23],
            },
            "Modifying to Add Details": {
                "Lesson": "LFC: Lesson 5",
                "Questions": [24, 25, 26],
            },
            "Connecting Ideas *Complex Sentences": {
                "Lesson": "LFC: Lesson 6",
                "Questions": [27, 28],
            },
            "Condensing Ideas": {"Lesson": "LFC: Lesson 7", "Questions": [29, 30]},
        }
    scores_by_skill = {}
    for key in qnum_dict:
        score = get_skill_average(qnum_dict[key]["Questions"], avg_by_question)
        scores_by_skill[key] = {"Lesson": qnum_dict[key]["Lesson"], "Score": score}

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

    if assessment_type == "ELD1_FLS" or assessment_type == "ELD2_FLS":
        detailed_skill = "Foundational Literacy Skills"
    elif assessment_type == "ELD1_CLS" or assessment_type == "ELD2_CLS":
        detailed_skill = "Collaborative Listening and Speaking"
    elif assessment_type == "ELD1_LFC" or assessment_type == "ELD2_LFC":
        detailed_skill = "Language Function and Construction"
    else:
        detailed_skill = "detailed skill unknown"

    data = {"Detailed Skill": [], "Connected Lesson": [], "Class Score": []}

    for skill, info in by_skill_dict.items():
        # We will filter out the 'Class Score' key because it doesn't contain lesson info
        if isinstance(info, dict) and "Lesson" in info:
            data["Detailed Skill"].append(skill)
            data["Connected Lesson"].append(info["Lesson"])
            data["Class Score"].append(info["Score"])
        else:
            overall_class_score = info

    # Add the overall class score row
    data["Detailed Skill"].append("Class Score")
    data["Connected Lesson"].append(None)
    data["Class Score"].append(overall_class_score)

    df = pd.DataFrame(data)

    return df


# if __name__ == "__main__":
# def main():
#     filepath = "../testingFiles/CLS1.csv"
#     assessment_type = "ELD1_CLS"
#     summary = report_from_file(filepath, assessment_type)
#     return summary


# main()
