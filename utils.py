from datetime import date, datetime, timedelta

def calculate_score(completed, rpe, weights_entered):
    score = 0
    if completed:
        score += 50
    if rpe > 0:
        score += min(int((rpe / 10) * 30), 30)
    if weights_entered:
        score += 20
    return score

def build_session_schedule(plan, start_date):
    all_sessions = []
    current_date = start_date
    training_days = plan.get("training_days", 3)
    for week in plan["weeks"]:
        for day in week["days"]:
            all_sessions.append({
                "session_id": f"w{week['week']}_d{day['day_number']}",
                "week": week["week"],
                "week_focus": week["focus"],
                "label": day["label"],
                "exercises": day["exercises"],
                "date": str(current_date)
            })
            gap = 7 // training_days
            current_date += timedelta(days=gap)
    return all_sessions

def get_today_session(all_sessions, log):
    today = date.today()
    for s in all_sessions:
        if s["date"] == str(today):
            return s
    for s in all_sessions:
        if s["date"] >= str(today) and s["session_id"] not in log:
            return s
    return None

def calculate_progress(all_sessions, log):
    total_sessions = len(all_sessions)
    completed_sessions = [s for s in all_sessions if log.get(s["session_id"], {}).get("completed")]
    total_completed = len(completed_sessions)
    overall_progress = int((total_completed / total_sessions) * 100) if total_sessions else 0
    total_score = sum(log.get(s["session_id"], {}).get("score", 0) for s in all_sessions)
    return total_completed, total_sessions, overall_progress, total_score