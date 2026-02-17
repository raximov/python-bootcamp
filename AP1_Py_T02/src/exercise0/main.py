#!/usr/bin/env python3
"""Task 1 — Exam Simulation using multiprocessing."""

import multiprocessing
import time
import random
import sys
import os

PHI = (1 + 5 ** 0.5) / 2  # Golden ratio ≈ 1.618


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def read_lines(filepath):
    """Read non-blank stripped lines from a text file."""
    with open(filepath, "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip()]


# ---------------------------------------------------------------------------
# Probability helpers
# ---------------------------------------------------------------------------

def golden_ratio_probs(n, is_boy):
    """Return a list of *n* probabilities following the golden-ratio rule.

    Boys: higher weight toward the beginning of the word list.
    Girls: higher weight toward the end (reversed).
    """
    if n <= 0:
        return []
    if n == 1:
        return [1.0]
    probs = []
    remaining = 1.0
    for _ in range(n - 1):
        p = remaining / PHI
        probs.append(p)
        remaining -= p
    probs.append(remaining)
    if not is_boy:
        probs.reverse()
    return probs


# ---------------------------------------------------------------------------
# Answer selection
# ---------------------------------------------------------------------------

def student_select_answer(words, is_boy):
    """Student picks one word from *words* using golden-ratio distribution."""
    weights = golden_ratio_probs(len(words), is_boy)
    return random.choices(words, weights=weights, k=1)[0]


def examiner_select_correct(words):
    """Examiner picks correct answers: one random word, then 1/3 chance to
    keep adding until stopped or all words chosen."""
    correct = set()
    correct.add(random.choice(words))
    while len(correct) < len(words) and random.random() < 1 / 3:
        remaining = [w for w in words if w not in correct]
        correct.add(random.choice(remaining))
    return correct


# ---------------------------------------------------------------------------
# Grading
# ---------------------------------------------------------------------------

def conduct_exam_for_student(questions, is_boy):
    """Ask 3 random questions, grade the student.

    Returns (passed: bool, question_results: list[(question, correct)])
    """
    selected = random.choices(questions, k=3)
    results = []
    correct_count = 0
    for q in selected:
        words = q.split()
        answer = student_select_answer(words, is_boy)
        correct_set = examiner_select_correct(words)
        ok = answer in correct_set
        results.append((q, ok))
        if ok:
            correct_count += 1

    roll = random.random()
    if roll < 1 / 8:
        passed = False                          # bad mood
    elif roll < 1 / 8 + 1 / 4:
        passed = True                           # good mood
    else:
        passed = correct_count > (3 - correct_count)  # neutral
    return passed, results


# ---------------------------------------------------------------------------
# Examiner process
# ---------------------------------------------------------------------------

def examiner_worker(examiner_name, name_len, student_queue,
                    shared_students, shared_examiners, shared_questions,
                    questions, lock, start_time):
    """Runs in a separate process. Pulls students from the queue, exams them,
    updates shared state through a Manager lock."""
    total = 0
    failed = 0
    lunch_taken = False

    while True:
        student_info = student_queue.get()       # blocks until available
        if student_info is None:                 # sentinel → stop
            break

        student_name, student_gender = student_info
        is_boy = student_gender == "M"

        # Tell display who we're examining
        with lock:
            ex = dict(shared_examiners[examiner_name])
            ex["current_student"] = student_name
            shared_examiners[examiner_name] = ex

        # Simulate exam duration
        exam_duration = random.uniform(name_len - 1, name_len + 1)
        time.sleep(exam_duration)

        # Grade
        passed, q_results = conduct_exam_for_student(questions, is_boy)
        total += 1
        if not passed:
            failed += 1

        finish_time = time.time() - start_time

        # ---- update shared state ----
        with lock:
            st = dict(shared_students[student_name])
            st["status"] = "Passed" if passed else "Failed"
            st["exam_duration"] = exam_duration
            st["finish_time"] = finish_time
            shared_students[student_name] = st

            for q, ok in q_results:
                qd = dict(shared_questions[q])
                qd["total"] = qd.get("total", 0) + 1
                if ok:
                    qd["correct"] = qd.get("correct", 0) + 1
                shared_questions[q] = qd

            ex = dict(shared_examiners[examiner_name])
            ex["current_student"] = "-"
            ex["total"] = total
            ex["failed"] = failed
            ex["work_time"] = round(finish_time, 2)
            shared_examiners[examiner_name] = ex

        # Lunch break: allowed after 30 s from exam start
        elapsed = time.time() - start_time
        if not lunch_taken and elapsed >= 30:
            lunch_taken = True
            with lock:
                ex = dict(shared_examiners[examiner_name])
                ex["current_student"] = "-"
                shared_examiners[examiner_name] = ex
            time.sleep(random.uniform(12, 18))

    # Mark done
    with lock:
        ex = dict(shared_examiners[examiner_name])
        ex["current_student"] = "-"
        ex["work_time"] = round(time.time() - start_time, 2)
        ex["done"] = True
        shared_examiners[examiner_name] = ex


# ---------------------------------------------------------------------------
# Table formatting
# ---------------------------------------------------------------------------

def format_table(headers, rows, alignments=None):
    """Pretty-print an ASCII table matching the README sample format."""
    ncols = len(headers)
    if alignments is None:
        alignments = ["center"] * ncols

    widths = [len(h) + 2 for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)) + 2)

    def _cell(text, w, align):
        s = str(text)
        if align == "left":
            return " " + s.ljust(w - 1)
        if align == "right":
            return s.rjust(w - 1) + " "
        return s.center(w)

    sep = "+" + "+".join("-" * w for w in widths) + "+"
    lines = [sep]
    lines.append("|" + "|".join(_cell(h, widths[i], alignments[i])
                                for i, h in enumerate(headers)) + "|")
    lines.append(sep)
    for row in rows:
        lines.append("|" + "|".join(_cell(c, widths[i], alignments[i])
                                    for i, c in enumerate(row)) + "|")
    lines.append(sep)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def _sorted_students(shared_students, student_order):
    """Return student dicts sorted: In queue → Passed → Failed."""
    data = []
    for name in student_order:
        d = dict(shared_students[name])
        d["name"] = name
        data.append(d)
    q = [s for s in data if s["status"] == "In queue"]
    p = [s for s in data if s["status"] == "Passed"]
    f = [s for s in data if s["status"] == "Failed"]
    q.sort(key=lambda x: x["order"])
    p.sort(key=lambda x: x.get("finish_time", 0))
    f.sort(key=lambda x: x.get("finish_time", 0))
    return q + p + f


def display_during(shared_students, shared_examiners,
                   examiner_order, student_order, start_time):
    sys.stdout.write("\033[H\033[J")
    students = _sorted_students(shared_students, student_order)

    rows = [(s["name"], s["status"]) for s in students]
    print(format_table(["Student", "Status"], rows, ["left", "center"]))
    print()

    ex_rows = []
    for name in examiner_order:
        ex = dict(shared_examiners[name])
        ex_rows.append((name, ex["current_student"],
                        str(ex["total"]), str(ex["failed"]),
                        f"{ex['work_time']:.2f}"))
    print(format_table(
        ["Examiner", "Current student", "Total students", "Failed", "Work time"],
        ex_rows, ["left", "left", "center", "center", "center"]))
    print()

    in_q = sum(1 for s in students if s["status"] == "In queue")
    print(f"Remaining in queue: {in_q} out of {len(students)}")
    print(f"Time since exam started: {time.time() - start_time:.2f}")
    sys.stdout.flush()


def display_final(shared_students, shared_examiners, shared_questions,
                  examiner_order, student_order, questions,
                  start_time, end_time):
    sys.stdout.write("\033[H\033[J")
    data = []
    for name in student_order:
        d = dict(shared_students[name])
        d["name"] = name
        data.append(d)

    passed = sorted([s for s in data if s["status"] == "Passed"],
                    key=lambda x: x.get("finish_time", 0))
    failed = sorted([s for s in data if s["status"] == "Failed"],
                    key=lambda x: x.get("finish_time", 0))

    rows = [(s["name"], s["status"]) for s in passed + failed]
    print(format_table(["Student", "Status"], rows, ["left", "center"]))
    print()

    ex_rows = []
    for name in examiner_order:
        ex = dict(shared_examiners[name])
        ex_rows.append((name, str(ex["total"]), str(ex["failed"]),
                        f"{ex['work_time']:.2f}"))
    print(format_table(
        ["Examiner", "Total students", "Failed", "Work time"],
        ex_rows, ["left", "center", "center", "center"]))
    print()

    total_time = end_time - start_time
    print(f"Time from exam start to finish: {total_time:.2f}")

    # Top-performing students — passed with the shortest exam duration
    if passed:
        min_dur = min(s["exam_duration"] for s in passed)
        top = [s["name"] for s in passed if s["exam_duration"] == min_dur]
        print(f"Top-performing students: {', '.join(top)}")
    else:
        print("Top-performing students: None")

    # Top examiners — lowest failure rate
    ex_stats = []
    for name in examiner_order:
        ex = dict(shared_examiners[name])
        rate = ex["failed"] / ex["total"] if ex["total"] else 0
        ex_stats.append((name, rate))
    min_rate = min(r for _, r in ex_stats)
    print(f"Top examiners: {', '.join(n for n, r in ex_stats if r == min_rate)}")

    # Students to be expelled — failed with the earliest finish time
    if failed:
        min_ft = min(s["finish_time"] for s in failed)
        expelled = [s["name"] for s in failed if s["finish_time"] == min_ft]
        print(f"Students to be expelled: {', '.join(expelled)}")
    else:
        print("Students to be expelled: None")

    # Best questions — highest correct count
    q_stats = []
    for q in questions:
        qd = dict(shared_questions[q])
        q_stats.append((q, qd.get("correct", 0)))
    max_c = max(c for _, c in q_stats) if q_stats else 0
    best = [q for q, c in q_stats if c == max_c]
    print(f"Best questions: {', '.join(best)}")

    # Result
    total_s = len(data)
    pass_pct = len(passed) / total_s if total_s else 0
    print(f"Result: {'Exam passed' if pass_pct > 0.85 else 'Exam failed'}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    examiner_lines = read_lines(os.path.join(script_dir, "examiners.txt"))
    student_lines = read_lines(os.path.join(script_dir, "students.txt"))
    questions = read_lines(os.path.join(script_dir, "questions.txt"))

    examiners = []
    for line in examiner_lines:
        parts = line.rsplit(maxsplit=1)
        examiners.append((parts[0], parts[1]))

    students = []
    for line in student_lines:
        parts = line.rsplit(maxsplit=1)
        students.append((parts[0], parts[1]))

    # ---- shared state via Manager ----
    mgr = multiprocessing.Manager()

    shared_students = mgr.dict()
    for i, (name, gender) in enumerate(students):
        shared_students[name] = {
            "status": "In queue", "gender": gender,
            "exam_duration": 0, "finish_time": 0, "order": i,
        }

    shared_examiners = mgr.dict()
    for name, _ in examiners:
        shared_examiners[name] = {
            "current_student": "-", "total": 0,
            "failed": 0, "work_time": 0.0, "done": False,
        }

    shared_questions = mgr.dict()
    for q in questions:
        shared_questions[q] = {"correct": 0, "total": 0}

    lock = mgr.Lock()

    # ---- student queue + sentinels ----
    student_queue = multiprocessing.Queue()
    for s in students:
        student_queue.put(s)
    for _ in examiners:
        student_queue.put(None)

    examiner_order = [n for n, _ in examiners]
    student_order = [n for n, _ in students]

    start_time = time.time()

    # ---- spawn examiner processes ----
    procs = []
    for name, _ in examiners:
        p = multiprocessing.Process(
            target=examiner_worker,
            args=(name, len(name), student_queue,
                  shared_students, shared_examiners, shared_questions,
                  questions, lock, start_time),
        )
        p.start()
        procs.append(p)

    # ---- live display loop ----
    while any(p.is_alive() for p in procs):
        display_during(shared_students, shared_examiners,
                       examiner_order, student_order, start_time)
        time.sleep(0.5)

    for p in procs:
        p.join()

    end_time = time.time()

    display_final(shared_students, shared_examiners, shared_questions,
                  examiner_order, student_order, questions,
                  start_time, end_time)


if __name__ == "__main__":
    main()
