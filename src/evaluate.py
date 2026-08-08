from query import retrieve_chunks, generate_answer

# Our evaluation set: (question, expected_answer_keywords, expected_page_or_section)
eval_set = [
    ("What is the minimum attendance required to sit for exams?", "75%", "Page 3 / Sec 7.1"),
    ("Below what attendance percentage can shortage NOT be condoned?", "65%", "Sec 7.4"),
    ("How many total credits are required to complete the B.Tech program?", "192", "Sec 4.3"),
    ("What CGPA is required for First Class with Distinction?", "7.75", "Sec 12.2"),
    ("What is the minimum SGPA/CGPA a student needs to pass?", "5.0", "Sec 8.6"),
    ("What happens if a student is caught using a mobile phone in the exam hall?", "Expulsion", "Sec 17"),
    ("What is the maximum number of years allowed to complete the B.Tech degree?", "8", "Sec 4.1"),
    ("How many credits are needed to get promoted from 1st year to 2nd year?", "50%", "Sec 8.3"),
    ("What is the passing minimum marks needed in the End Semester Exam for a theory subject?", "35%", "Sec 8.1"),
    ("What happens if a student impersonates another candidate in an exam?", "Expelled", "Sec 17"),
    ("What is the minimum percentage of marks needed for Industry-Oriented Mini-Project/Seminar?", "40%", "Sec 8.2"),
    ("How many credits does a student typically register for per semester from 3rd year onwards?", "24", "Sec 5.4"),
    ("What is the duration of the End Semester Examination for theory subjects?", "3 hours", "Sec 9.3.a"),
    ("Who conducts the Comprehensive Viva-Voce examination?", "Head of the Department", "Sec 9.8"),
    ("What percentage range corresponds to 80% and above grade band?", "80%", "Sec 10.2"),
    ("Can a student repeat a subject just to improve their grade?", "not be permitted", "Sec 10.5"),
    ("What is required for NCC/NSS/NSO courses to get a Satisfactory Participation Certificate?", "65%", "Sec 9.11"),
    ("How many marks are allotted for internal evaluation vs external for practical subjects?", "30", "Sec 9.4"),
    ("What happens if a student is absent for a mid-term exam?", "substitution test", "Sec 9.3.a"),
    ("What CGPA range is needed for Second Class?", "5.75", "Sec 12.2"),
]

def run_evaluation():
    results = []
    for i, (question, expected_keyword, expected_source) in enumerate(eval_set, 1):
        print(f"Running {i}/{len(eval_set)}: {question}")
        chunks = retrieve_chunks(question)
        answer = generate_answer(question, chunks)

        # Simple check: does the expected keyword appear in the generated answer?
        found = expected_keyword.lower() in answer.lower()

        results.append({
            "question": question,
            "answer": answer,
            "expected_keyword": expected_keyword,
            "expected_source": expected_source,
            "correct": found
        })

    return results


import json

def print_report(results):
    correct_count = sum(1 for r in results if r["correct"])
    total = len(results)
    accuracy = (correct_count / total) * 100

    print("\n" + "="*60)
    print(f"EVALUATION REPORT: {correct_count}/{total} correct ({accuracy:.1f}%)")
    print("="*60 + "\n")

    for i, r in enumerate(results, 1):
        status = "CORRECT" if r["correct"] else "INCORRECT"
        print(f"[{status}] Q{i}: {r['question']}")
        print(f"Answer: {r['answer']}")
        print()

    return accuracy


def save_results(results, accuracy):
    # Save as JSON (for code/data use)
    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump({"accuracy": accuracy, "results": results}, f, indent=2)

    # Save as readable text (for your README/report)
    with open("evaluation_results.txt", "w", encoding="utf-8") as f:
        f.write(f"EVALUATION REPORT: {sum(1 for r in results if r['correct'])}/{len(results)} correct ({accuracy:.1f}%)\n")
        f.write("="*60 + "\n\n")
        for i, r in enumerate(results, 1):
            status = "CORRECT" if r["correct"] else "INCORRECT"
            f.write(f"[{status}] Q{i}: {r['question']}\n")
            f.write(f"Expected source: {r['expected_source']}\n")
            f.write(f"Full Answer: {r['answer']}\n\n")

    print("\nSaved full results to evaluation_results.json and evaluation_results.txt")


if __name__ == "__main__":
    results = run_evaluation()
    accuracy = print_report(results)
    save_results(results, accuracy)
if __name__ == "__main__":
    results = run_evaluation()
    print_report(results)